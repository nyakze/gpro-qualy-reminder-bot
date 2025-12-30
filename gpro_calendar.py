import json
import logging
import re
import os
from datetime import datetime, timedelta
import aiohttp
from config import GPRO_API_TOKEN, CALENDAR_FILE, GPRO_LANG, NEXT_SEASON_FILE

logger = logging.getLogger(__name__)

# Module-level globals
race_calendar = {}
next_season_calendar = {}


async def load_calendar_silent() -> bool:
    """Load from cache ONLY - no API calls"""
    try:
        with open(CALENDAR_FILE, 'r') as f:
            data = json.load(f)
            calendar = {}
            for race_id_str, race_data in data.items():
                race_id = int(race_id_str)
                calendar[race_id] = {
                    'quali_close': datetime.fromisoformat(race_data['quali_close']),
                    'track': race_data['track'],
                    'date': datetime.fromisoformat(race_data['date']),
                    'group': race_data.get('group', 'Pro')
                }
            global race_calendar
            race_calendar.clear()
            race_calendar.update(calendar)
            logger.info(f"✅ Loaded {len(calendar)} races from cache")
            return True
    except FileNotFoundError:
        logger.warning("No cache file - use /calendar")
        return False
    except Exception as e:
        logger.error(f"Cache load error: {e}")
        return False

async def load_next_season_silent() -> bool:
    """Load next season from cache ONLY"""
    try:
        if os.path.exists(NEXT_SEASON_FILE):
            with open(NEXT_SEASON_FILE, 'r') as f:
                data = json.load(f)
                calendar = {}
                for race_id_str, race_data in data.items():
                    race_id = int(race_id_str)
                    calendar[race_id] = {
                        'quali_close': datetime.fromisoformat(race_data['quali_close']),
                        'track': race_data['track'],
                        'date': datetime.fromisoformat(race_data['date']),
                        'group': race_data.get('group', 'Pro')
                    }
                global next_season_calendar
                next_season_calendar.clear()
                next_season_calendar.update(calendar)
                logger.info(f"✅ Loaded {len(calendar)} next season races from cache")
                return True
        return False
    except Exception as e:
        logger.error(f"Next season cache load error: {e}")
        return False

async def update_calendar() -> bool:
    """Update calendar from GPRO API - /update command"""
    if not GPRO_API_TOKEN:
        logger.error("❌ GPRO_API_TOKEN missing")
        return False
        
    url = f"https://gpro.net/{GPRO_LANG}/backend/api/v2/Calendar"
    headers = {
        "Authorization": f"Bearer {GPRO_API_TOKEN}",
        "User-Agent": "GPRO-QualiBot/1.0"
    }
    
    try:
        logger.info("🔄 Updating calendar from GPRO API...")
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    raw_response = await resp.json()
                    
                    # CURRENT SEASON
                    data = raw_response.get('events', [])
                    calendar = parse_gpro_events(data, is_next_season=False)
                    
                    if calendar:
                        save_calendar(calendar)
                        global race_calendar
                        race_calendar.clear()
                        race_calendar.update(calendar)
                        logger.info(f"✅ CURRENT SEASON: {len(calendar)} races!")
                    else:
                        logger.warning("No valid race events found")
                    
                    # NEXT SEASON LOGIC
                    next_season_published = raw_response.get("nextSeasonPublished", False)
                    logger.info(f"📊 API nextSeasonPublished: {next_season_published}")
                    
                    if next_season_published:
                        next_events = raw_response.get("nextSeasonEvents", [])
                        logger.info(f"📊 Found {len(next_events)} nextSeasonEvents")
                        
                        if next_events:
                            next_calendar = parse_gpro_events(next_events, is_next_season=True)
                            if next_calendar:
                                save_next_season_calendar(next_calendar)
                                global next_season_calendar
                                next_season_calendar.clear()
                                next_season_calendar.update(next_calendar)
                                logger.info(f"🌟 NEXT SEASON: {len(next_calendar)} races populated!")
                            else:
                                logger.warning("No valid next season events")
                        else:
                            logger.warning("nextSeasonPublished=true but no nextSeasonEvents")
                    else:
                        # FORCE CLEANUP
                        next_season_calendar.clear()
                        
                        if os.path.exists(NEXT_SEASON_FILE):
                            os.remove(NEXT_SEASON_FILE)
                            logger.info("🗑️ Next season file REMOVED - API says not published")
                        else:
                            logger.info("ℹ️ No next season file (already clean)")
                    
                    return True
                else:
                    logger.error(f"API {resp.status}")
    except Exception as e:
        logger.error(f"Calendar update error: {e}")
    
    return False

def parse_gpro_events(events: list, is_next_season: bool = False) -> dict:
    """Parse GPRO events - SEQUENTIAL RACE NUMBERS 1,2,3...!"""
    calendar = {}
    valid_races = []
    season_type = "🌟 NEXT" if is_next_season else "✅ CURRENT"
    
    # **1. COLLECT ALL valid races first**
    for event in events:
        if event.get('eventType') != 'R':  # Race only
            continue
            
        idx = event.get('idxReal') or event.get('idx')
        if not idx:
            continue
            
        date_str = event.get('dateEvent')
        track = event.get('trackName', f"Race {idx}")
        
        try:
            race_date = parse_gpro_date_fixed(date_str)
            if not race_date:
                continue
                
            # ADD 19:00 UTC race time
            race_date = race_date.replace(hour=19, minute=0, second=0)
            quali_close = race_date - timedelta(hours=1.5)
            
            valid_races.append({
                'orig_id': int(idx),
                'quali_close': quali_close,
                'track': track[:30],
                'date': race_date,
                'group': event.get('group', 'Pro')
            })
        except Exception as e:
            logger.debug(f"Parse event {idx} error: {e}")
            continue
    
    # **2. SORT by date + RE-NUMBER 1,2,3...**
    valid_races.sort(key=lambda x: x['date'])
    
    for seq_num, race_data in enumerate(valid_races, 1):
        calendar[seq_num] = {
            'quali_close': race_data['quali_close'],
            'track': race_data['track'],
            'date': race_data['date'],
            'group': race_data['group']
        }
        logger.info(f"{season_type} Race {seq_num}: {race_data['track']} → {race_data['date'].strftime('%d.%m %Y 19:00 UTC')}")
    
    logger.info(f"{season_type} Parsed {len(calendar)} sequential race events at 19:00 UTC")
    return calendar

def parse_gpro_date_fixed(date_str: str) -> datetime:
    """Parse GPRO dates - Simple 'Today' handler!"""
    if not date_str:
        return None
    
    # **SIMPLE "Today" = CURRENT DAY 00:00**
    if 'Today' in date_str or '<font' in date_str or '<b>' in date_str:
        now = datetime.utcnow()
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        logger.info(f"⏰ 'Today' → {today.strftime('%d.%m.%Y')} UTC 19:00")
        return today
        
    # **CLEAN HTML + ordinals**
    day_str = re.sub(r'<[^>]*>', '', date_str)
    day_str = re.sub(r'(?i)(st|nd|rd|th)\b', '', day_str)
    day_str = day_str.strip()
    
    now = datetime.utcnow()
    
    # **YOUR WORKING FORMATS**
    formats = [
        '%d.%m %Y',    # 05.12 2025
        '%b %d, %Y', 
        '%b %d %Y', 
        '%d %b %Y',
        '%Y-%m-%d', 
        '%d.%m.%Y'
    ]
    
    for fmt in formats:
        try:
            dt = datetime.strptime(day_str, fmt)
            if dt.year < 2025:
                dt = dt.replace(year=now.year)
            return dt
        except ValueError:
            continue
    
    # Month/day only
    if not re.search(r'\d{4}', day_str):
        try:
            dt = datetime.strptime(day_str, '%b %d')
            dt = dt.replace(year=now.year)
            if dt.date() < now.date():
                dt = dt.replace(year=now.year + 1)
            return dt
        except:
            pass
    
    logger.warning(f"Cannot parse date: '{date_str}'")
    return None

def save_calendar(calendar: dict):
    """Save calendar"""
    serializable = {}
    for k, v in calendar.items():
        serializable[str(k)] = {
            'quali_close': v['quali_close'].isoformat(),
            'track': v['track'],
            'date': v['date'].isoformat(),
            'group': v['group']
        }
    with open(CALENDAR_FILE, 'w') as f:
        json.dump(serializable, f, indent=2)
    logger.info(f"💾 Saved current season to {CALENDAR_FILE}")

def save_next_season_calendar(calendar: dict):
    """Save NEXT season calendar"""
    serializable = {}
    for k, v in calendar.items():
        serializable[str(k)] = {
            'quali_close': v['quali_close'].isoformat(),
            'track': v['track'],
            'date': v['date'].isoformat(),
            'group': v['group']
        }
    with open(NEXT_SEASON_FILE, 'w') as f:
        json.dump(serializable, f, indent=2)
    logger.info(f"💾 Saved next season to {NEXT_SEASON_FILE}")

def get_races_closing_soon(hours_before: float = 720) -> dict:
    """Get races closing within 30 days - SORTED by time!"""
    now = datetime.utcnow()
    upcoming = {}
    
    for race_id, data in race_calendar.items():
        time_to_close = (data['quali_close'] - now).total_seconds() / 3600
        if 0 < time_to_close <= hours_before:
            data_copy = data.copy()
            data_copy['hours_left'] = time_to_close
            upcoming[race_id] = data_copy
    
    # Sort by closest first
    sorted_upcoming = dict(sorted(upcoming.items(), key=lambda x: x[1]['hours_left']))
    logger.info(f"Upcoming races ({len(sorted_upcoming)}): {list(sorted_upcoming.keys())}")
    return sorted_upcoming

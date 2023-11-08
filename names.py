class Columns:
    # Hits
    SESSION_ID = 'session_id'
    CLIENT_ID = 'client_id'
    VISIT_DATE = 'visit_date'
    VISIT_TIME = 'visit_time'
    VISIT_NUMBER = 'visit_number'
    UTM_SOURCE = 'utm_source'
    UTM_MEDIUM = 'utm_medium'
    UTM_CAMPAIGN = 'utm_campaign'
    UTM_ADCONTENT = 'utm_adcontent'
    UTM_KEYWORD = 'utm_keyword'
    DEVICE_CATEGORY = 'device_category'
    DEVICE_OS = 'device_os'
    DEVICE_BRAND = 'device_brand'
    DEVICE_MODEL = 'device_model'
    DEVICE_SCREEN_RESOLUTION = 'device_screen_resolution'
    DEVICE_BROWSER = 'device_browser'
    GEO_COUNTRY = 'geo_country'
    GEO_CITY = 'geo_city'

    # Sessions
    SESSION_ID = 'session_id'
    HIT_DATE = 'hit_date'
    HIT_TIME = 'hit_time'
    HIT_NUMBER = 'hit_number'
    HIT_TYPE = 'hit_type'
    HIT_REFERER = 'hit_referer'
    HIT_PAGE_PATH = 'hit_page_path'
    EVENT_CATEGORY = 'event_category'
    EVENT_LABEL = 'event_label'
    EVENT_VALUE = 'event_value'

    HOW_MANY_TIMES_VISITED_STR = 'how_many_times_visited'
    HOW_MANY_TIMES_VISITED_INT = 'how_many_times_visited_int'

    IS_FROM_RUSSIA_INT = 'is_from_russia'

    VISIT_DATE_DT = 'visit_date_dt'
    VISIT_DATE_YEAR = 'visit_date_year'
    VISIT_DATE_MONTH = 'visit_date_month'
    VISIT_DATE_DAY = 'visit_date_day'
    VISIT_DATE_WEEKDAY = 'visit_date_weekday'

    VISIT_TIME_DT = 'visit_time_dt'
    VISIT_TIME_HOURS = 'visit_time_hours'
    VISIT_TIME_MINUTES = 'visit_time_minutes'
    VISIT_TIME_SECONDS = 'visit_time_seconds'
    VISIT_TIME_FULL_HOURS = 'visit_time_full_hours'
    VISIT_TIME_FULL_MINUTES = 'visit_time_full_minutes'

    UTM_CAMPAIGN_CUSTOMISED = 'utm_campaign_customised'
    UTM_SOURCE_CUSTOMISED = 'utm_source_customised'
    UTM_MEDIUM_CUSTOMISED = 'utm_medium_customised'
    UTM_ADCONTENT_CUSTOMISED = 'utm_adcontent_customised'
    UTM_KEYWORD_CUSTOMISED = 'utm_keyword_customised'
    DEVICE_BRAND_CUSTOMISED = 'device_brand_customised'
    GEO_CITY_CUSTOMISED = 'geo_city_customised'

    DEVICE_SCREEN_RESOLUTION_MULT = 'device_screen_resolution_mult'

    RANDOM_NUMBER_FROM_0_TO_1 = 'random_number_from_0-1'

    IS_TARGET = 'is_target'


c = Columns()
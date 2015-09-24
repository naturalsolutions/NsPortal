

### test if the match url is integer
def integers(*segment_names):
    def predicate(info, request):
        match = info['match']
        for segment_name in segment_names:
            try:
                print (segment_names)
                match[segment_name] = int(match[segment_name])
                if int(match[segment_name]) == 0 :
                    print(' ****** ACTIONS FORMS ******')
                    return False
            except (TypeError, ValueError):
                return False
        return True
    return predicate

def add_routes(config):
    config.add_route('weekData', 'ecoReleve-Sensor/weekData')
    
    ##### Security routes #####
    config.add_route('security/login', 'ecoReleve-Core/security/login')
    config.add_route('security/logout', 'ecoReleve-Core/security/logout')
    config.add_route('security/has_access', 'ecoReleve-Core/security/has_access')

    ##### User #####
    config.add_route('core/user', 'ecoReleve-Core/user')
    config.add_route('core/currentUser', 'ecoReleve-Core/currentUser')


    ##### Site #####
    config.add_route('core/site', 'ecoReleve-Core/site')
    config.add_route('core/instance', 'ecoReleve-Core/instance')







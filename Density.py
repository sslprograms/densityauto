import requests, threading, string, random, os, json, subprocess, autoselenium, time

config = json.loads(
    open('Config.json', 'r').read()
)

os.system('mode con:cols=60 lines=20')

cookies = open(config['cookies']['file'], 'r').read().splitlines()
proxies = open(config['proxies']['file'], 'r').read().splitlines()


tasks = 0

def format_upc(__lib__):
    newLib = []
    for string in __lib__:
        cookie = '_|' + string.split('_|')[1]
        newLib.append(cookie)


    return newLib

if config['cookies']['upc'] == True:
    cookies = format_upc(cookies)

PROXY_TYPE = config['proxies']['type']


def getCaptchaDetails():
    with requests.session() as session:

        proxy = {}

        if config['settings'][0]['cookie_gen']['proxies'] == True:
            __proxy_type__ = PROXY_TYPE
            proxy = {'http':f'{__proxy_type__}://{random.choice(proxies)}', 'https':f'{__proxy_type__}://{random.choice(proxies)}'}

        JSONSignup = {
            "agreementIds":[
                "848d8d8f-0e33-4176-bcd9-aa4e22ae7905",
                "54d8a8f0-d9c8-4cf3-bd26-0cbf8af0bba3"
            ],

            "birthday":"21 Sep 2006",
            "context":"MultiverseSignupForm",
            "displayAvatarV2":False,
            "displayContextV2":False,
            "gender":2,
            "isTosAgreementBoxChecked":True,
            "password":'testpasswordrec',
            "username":''.join(random.choices(string.ascii_lowercase + string.digits + string.ascii_uppercase, k=10)),
            "referralData":None,
            'abTestVariation':0
        }

        session.proxies = proxy
        session.headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30'
        }

        site_token = session.post(
            'https://auth.roblox.com/v1/usernames/validate'
        ).headers['x-csrf-token']
        
        captchaDetails = session.post(
            'https://auth.roblox.com/v2/signup',

            headers = session.headers.update({
                'x-csrf-token':site_token
            }),
        
            json = JSONSignup

        ).json()['failureDetails'][0]['fieldData'].split(',')

        captchaId = captchaDetails[0]
        captchaBlob = captchaDetails[1]

        session.headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30',
            'origin':'https://www.roblox.com',
            'referer':'https://www.roblox.com/'
        }

        getToken = session.post(
            'https://roblox-api.arkoselabs.com/fc/gt2/public_key/A2A14B1D-1AF3-C791-9BBC-EE33CC7A0A6F',

            data = {
                'public_key':'A2A14B1D-1AF3-C791-9BBC-EE33CC7A0A6F',
                'userbrowser': session.headers['user-agent'],
                'rnd':f'0.{random.randint(1000,10000000)}',
                'data[blob]':captchaBlob,
                'language':'en'
            }
        ).json()['token']

    return {'token':getToken, 'captchaId':captchaId, 'captchaBlob':captchaBlob}


def signup_roblox(captchaId, captcha_token):
    with requests.session() as session:

        proxy = {}

        if config['settings'][0]['cookie_gen']['proxies'] == True:
            __proxy_type__ = PROXY_TYPE
            proxy = {'http':f'{__proxy_type__}://{random.choice(proxies)}', 'https':f'{__proxy_type__}://{random.choice(proxies)}'}

        username = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=random.randint(7, 19)))
        password = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=10))

        session.headers['x-csrf-token'] = session.post(
            'https://auth.roblox.com/v1/usernames/validate'
        ).headers['x-csrf-token']

        session.headers['referer'] = 'https://www.roblox.com/'
        session.headers['origin'] = 'https://www.roblox.com'

        JSONSignup = {
            "agreementIds":[
                "848d8d8f-0e33-4176-bcd9-aa4e22ae7905",
                "54d8a8f0-d9c8-4cf3-bd26-0cbf8af0bba3"
            ],

            "birthday":"21 Sep 2006",
            "context":"MultiverseSignupForm",
            "displayAvatarV2":False,
            "displayContextV2":False,
            "gender":2,
            "isTosAgreementBoxChecked":True,
            "password":password,
            "username":username,
            "referralData":None,
            'abTestVariation':0,
            'captchaId':captchaId,
        }

        JSONSignup.update({"captchaProvider":"PROVIDER_ARKOSE_LABS", "captchaToken":str(captcha_token)})

        create = session.post(
            'https://auth.roblox.com/v2/signup',

            json = JSONSignup

        )

        print('\n\n' + str(JSONSignup) + '\n\n')

        if create.status_code == 200:
            print(create.text)
            cookie = session.cookies['.ROBLOSECURITY']
            writer = f'{cookie}'

            if config['settings'][0]['cookie_gen']['upc'] == True:
                writer = username + ':' + password + ':' + cookie

            open(config['settings'][0]['cookie_gen']['output'], 'a').write(writer+'\n')

            report = session.patch(
                'https://captchagrinder.com/api/report',

                data = {
                    'blob':f'{username}:{password}:{cookie}'
                }
            )





def solve_captcha(token, captchaId, captchaBlob):
    browser = config['settings'][0]['cookie_gen']['browser']
    driver = autoselenium.Driver(browser)    
    location = token.split('|')[1]
    token_id = token.split('|')[0]
    solver_url = f'https://roblox-api.arkoselabs.com/fc/gc/?token={token_id}&{location}&lang=en&pk=A2A14B1D-1AF3-C791-9BBC-EE33CC7A0A6F&cdn_url=https%3A%2F%2Froblox-api.arkoselabs.com%2Fcdn%2Ffc'
    print(f'- Received Captcha Details!\n\n\nCaptchaId : {captchaId}\nCaptchaBlob : {captchaBlob}\nLocation : {location}\ntoken : {token_id}\n\n\n(Starting selenium browser to solve the captcha)..\n\n\n')
    driver.get(solver_url)
    time.sleep(3)
    print('\n\n[PRESS ENTER]: Press return/enter key on your keyboard if you finished the captcha!')
    input()
    driver.quit()
    threading.Thread(target=signup_roblox, args=(captchaId, token,)).start()



def select_cookie_gen():
    print('\n\n> Started...')
    while True:
        details =getCaptchaDetails()
        solve_captcha(details['token'], details['captchaId'], details['captchaBlob'])


def check_cookie(cookie):
    try:
        global tasks
        with requests.session() as session:
            session.cookies['.ROBLOSECURITY'] = cookie
            
            session.headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.44'

            checker = session.get(
                'https://users.roblox.com/v1/users/authenticated',
            )

            if checker.status_code == 200:
                userId = checker.json()['id']
                print(f'> Valid | {userId}')
                open(config['settings'][0]['cookie_checker']['output'], 'a').write(cookie + '\n')

            tasks -= 1
    except:
        tasks -= 1

def select_cookie_checker():
    global tasks
    print('\n\n> Started...')
    for x in cookies:
        threading.Thread(target=check_cookie, args=(x,)).start()
        tasks += 1
    
    while True:
        time.sleep(1)
        if tasks <= 0:
            break
    
    print('\n\n[FINISHED] > Press enter/return to go to the main screen!')
    input()
    return

def check_poxy(proxy):
    global tasks
    with requests.session() as session:
        try:
            __proxy_type__ = PROXY_TYPE
            session.proxies = {'http':f'{__proxy_type__}://{proxy}', 'https':f'{__proxy_type__}://{proxy}'}
            checker = session.get('https://www.roblox.com', timeout=500)
            if checker.status_code == 200:
                print(f'> Valid | {proxy} | {PROXY_TYPE}')
                open(config['settings'][0]['proxy_checker']['output'], 'a').write(proxy + '\n')
            tasks -= 0
        except:
            tasks -= 0
            print(f'> Bad Proxy | {proxy} | {PROXY_TYPE}')


def select_proxy_checker():
    global tasks
    print('\n\n> Started...')
    for x in proxies:
        threading.Thread(target=check_poxy, args=(x,)).start()
        tasks += 1
    
    while True:
        time.sleep(1)
        if tasks <= 0:
            break
    
    print('\n\n[FINISHED] > Press enter/return to go to the main screen!')
    input()
    return


def buy_model(cookie, asset, userid, product):
    global tasks
    try:
        with requests.session() as session:
            session.cookies['.ROBLOSECURITY'] = cookie
            session.headers['x-csrf-token'] = session.post('https://friends.roblox.com/v1/users/1/request-friendship').headers['x-csrf-token']
            proxy = random.choice(proxies)
            __proxy_type__ = PROXY_TYPE
            session.proxies = {'http':f'{__proxy_type__}://{proxy}', 'https':f'{__proxy_type__}://{proxy}'}

            buy = session.post(
                f'https://economy.roblox.com/v1/purchases/products/{product}',

                data = {
                    'expectedCurrency':1,
                    'expectedPrice':0,
                    'expectedSellerId':userid
                }
            )

            if buy.status_code == 200:
                print(f'> Asset Bought | {product}')

                session.proxies = {}

                delete = session.post(
                    'https://www.roblox.com/asset/delete-from-inventory',
                    
                    data = {
                        'assetId':asset
                    }
                )

            else:
                print(f'> Failed Purchase | {product}')
            
            tasks -= 1
    except:
        tasks -= 1

def select_model_bot():
    global tasks
    print('> Enter AssetId: ')
    assetId = input('-: ')
    print('> Enter amount of sales: ')
    sales = input('-: ')

    print('\n\n> Started...')

    site_token = requests.post(
                'https://auth.roblox.com/v1/usernames/validate'
            ).headers['x-csrf-token']

    product_info = requests.post(
        'https://catalog.roblox.com/v1/catalog/items/details',

        headers = {
            'x-csrf-token':site_token
        },

        json = {
            "items":[
                {
                    "itemType":"Asset",
                    "id":assetId
                }
            ]
        }
    )

    user = product_info.json()['data'][0]['creatorTargetId']
    productId = product_info.json()['data'][0]['productId']

    for __round__ in range(int(sales)):
        threading.Thread(target=buy_model, args=(random.choice(cookies), assetId, user, productId,)).start()
        tasks += 1

    while True:
        time.sleep(1)
        if tasks <= 0:
            break
    
    print('\n\n[FINISHED] > Press enter/return to go to the main screen!')
    input()
    return
    

def send_favorite(cookie, assetId):
    global tasks
    try:
        with requests.session() as session:
            session.cookies['.ROBLOSECURITY'] = cookie
            session.headers['x-csrf-token'] = session.post('https://friends.roblox.com/v1/users/1/request-friendship').headers['x-csrf-token']
            proxy = random.choice(proxies)
            __proxy_type__ = PROXY_TYPE
            session.proxies = {'http':f'{__proxy_type__}://{proxy}', 'https':f'{__proxy_type__}://{proxy}'}

            favorite = session.post(
                'https://www.roblox.com/favorite/toggle',

                data = {
                    'assetID':assetId
                }
            )

            if favorite.status_code == 200:
                print(f'> Toggled Favorite | {assetId}')
            else:
                print(f'> Failed Toggle | {assetId}')
        tasks -= 1
    except:
        tasks -= 1

def select_favorite_bot():
    global tasks
    print('> Enter AssetId: ')
    assetId = input('-: ')
    print('\n\n> Started...')
    for x in cookies:
        threading.Thread(target=send_favorite, args=(x,assetId,)).start()
        tasks += 1
    
    while True:
        time.sleep(1)
        if tasks <= 0:
            break
    
    print('\n\n[FINISHED] > Press enter/return to go to the main screen!')
    input()
    return

def select_visit_bot():
    print('> Enter GameId: ')
    gameId = input('-: ')
    print('> Enter Target Visits: ')
    visits = input('-: ')

    for x in range(int(visits)):
        with requests.session() as session:
            session.cookies['.ROBLOSECURITY'] = random.choice(cookies)
            session.headers['x-csrf-token'] = session.post('https://friends.roblox.com/v1/users/1/request-friendship').headers['x-csrf-token']
            session.headers['referer'] = 'https://www.roblox.com/'

            ticket = session.post(
                'https://auth.roblox.com/v1/authentication-ticket/'
            ).headers['rbx-authentication-ticket']

            os.startfile(f'roblox-player:1+launchmode:play+gameinfo:{ticket}+launchtime:{random.randint(10000,1000000)}+placelauncherurl:https%3A%2F%2Fassetgame.roblox.com%2Fgame%2FPlaceLauncher.ashx%3Frequest%3DRequestGame%26browserTrackerId%3D119363552595%26placeId%3D{gameId}%26isPlayTogetherGame%3Dfalse+browsertrackerid:119363552595+robloxLocale:en_us+gameLocale:en_us+channel:')

            print(f'> Launched Cookie | roblox-player')

            time.sleep(14)

def send_friend(cookie, userId):
    global tasks
    with requests.session() as session:
        session.cookies['.ROBLOSECURITY'] = cookie
        session.headers['x-csrf-token'] = session.post('https://friends.roblox.com/v1/users/1/request-friendship').headers['x-csrf-token']

        send = session.post(
            f'https://friends.roblox.com/v1/users/{userId}/request-friendship'
        )

        if send.status_code == 200:
            print(f'> Sent Friend | {userId}')
        else:
            print(f'> Failed Friend | {userId}')

        tasks -= 1

def select_friend_bot():
    global tasks
    print('> Enter UserId: ')
    userId = input('-: ')
    print('\n\n> Started...')
    for x in cookies:
        threading.Thread(target=send_friend, args=(x,userId,)).start()
        tasks += 1
    
    while True:
        time.sleep(1)
        if tasks <= 0:
            break
    
    print('\n\n[FINISHED] > Press enter/return to go to the main screen!')
    input()
    return



def getCaptchaDetailsFromFollow(cookie, UserId):
    with requests.session() as session:

        session.cookies['.ROBLOSECURITY'] = cookie

        proxy = {}

        if config['settings'][0]['follow_bot']['proxies'] == True:
            __proxy_type__ = PROXY_TYPE
            proxy = {'http':f'{__proxy_type__}://{random.choice(proxies)}', 'https':f'{__proxy_type__}://{random.choice(proxies)}'}

        session.proxies = proxy
        session.headers['x-csrf-token'] = session.post('https://friends.roblox.com/v1/users/1/request-friendship').headers['x-csrf-token']
        
        captchaDetails = session.post(
            f'https://friends.roblox.com/v1/users/{UserId}/follow',


        ).json()['errors'][0]['fieldData']

        captchaId = captchaDetails.split('\",\"unifiedCaptchaId\":\"')[1].split('\"}"}]')[0].split('"}')[0]
        print(captchaId)
        captchaBlob = captchaDetails.split('"{\"dxBlob\":\"')[0].split('\",')[0].split('{"dxBlob":"')[1]
        print(captchaBlob)

        session.headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30',
            'origin':'https://www.roblox.com',
            'referer':'https://www.roblox.com/'
        }

        getToken = session.post(
            'https://roblox-api.arkoselabs.com/fc/gt2/public_key/63E4117F-E727-42B4-6DAA-C8448E9B137F',

            data = {
                'public_key':'63E4117F-E727-42B4-6DAA-C8448E9B137F',
                'userbrowser': session.headers['user-agent'],
                'rnd':f'0.{random.randint(1000,10000000)}',
                'data[blob]':captchaBlob,
                'language':'en'
            }
        ).json()['token']

    return {'token':getToken, 'captchaId':captchaId, 'captchaBlob':captchaBlob}

def follow_user(cookie, userId, captchaId, captchaToken):
    try:
        with requests.session() as session:
            session.cookies['.ROBLOSECURITY'] = cookie
            session.headers['x-csrf-token'] = session.post('https://friends.roblox.com/v1/users/1/request-friendship').headers['x-csrf-token']
            proxy = {}
            if config['settings'][0]['follow_bot']['proxies'] == True:
                __proxy_type__ = PROXY_TYPE
                proxy = {'http':f'{__proxy_type__}://{random.choice(proxies)}', 'https':f'{__proxy_type__}://{random.choice(proxies)}'}

            session.proxies = proxy

            follow = session.post(
                f'https://friends.roblox.com/v1/users/{userId}/follow',

                data = {
                    'captchaId':captchaId,
                    'captchaToken':captchaToken,
                    'captchaProvider':'PROVIDER_ARKOSE_LABS'
                }
            )

            print(follow.text)

            if follow.status_code == 200:
                print(f'> Added Follow | {userId} | {captchaId}')
            else:
                print(f'> Failed Follow | {captchaId}')
    except:
        pass


def solve_captcha_follow(token, captchaId, captchaBlob, cookie, userId):
    driver = autoselenium.Driver('edge')    
    location = token.split('|')[1]
    token_id = token.split('|')[0]
    solver_url = f'https://roblox-api.arkoselabs.com/fc/gc/?token={token_id}&{location}&lang=en&pk=A2A14B1D-1AF3-C791-9BBC-EE33CC7A0A6F&cdn_url=https%3A%2F%2Froblox-api.arkoselabs.com%2Fcdn%2Ffc'
    print(f'- Received Captcha Details!\n\n\nCaptchaId : {captchaId}\nCaptchaBlob : {captchaBlob}\nLocation : {location}\ntoken : {token_id}\n\n\n(Starting selenium browser to solve the captcha)..\n\n\n')
    driver.get(solver_url)
    time.sleep(3)
    print('\n\n[PRESS ENTER]: Press return/enter key on your keyboard if you finished the captcha!')
    input()
    driver.quit()
    threading.Thread(target=follow_user, args=(cookie, userId, captchaId, token,)).start()

def select_follower_bot():
    print('> Enter UserId: ')
    userId = input('-: ')
    print('\n\n> Started...')
    for x in cookies:
        try:
            captchaInfo = getCaptchaDetailsFromFollow(x, userId)
            token = captchaInfo['token']
            captchaBlob = captchaInfo['captchaBlob']
            captchaId = captchaInfo['captchaId']
            solve_captcha_follow(token, captchaId, captchaBlob, x, userId)
        except:
            pass

    
    print('\n\n[FINISHED] > Press enter/return to go to the main screen!')
    input()
    return













def getCaptchaDetailsFromGroup(cookie, groupId):
    with requests.session() as session:

        session.cookies['.ROBLOSECURITY'] = cookie

        proxy = {}

        if config['settings'][0]['group_join_bot']['proxies'] == True:
            __proxy_type__ = PROXY_TYPE
            proxy = {'http':f'{__proxy_type__}://{random.choice(proxies)}', 'https':f'{__proxy_type__}://{random.choice(proxies)}'}

        session.proxies = proxy
        session.headers['x-csrf-token'] = session.post('https://friends.roblox.com/v1/users/1/request-friendship').headers['x-csrf-token']
        
        captchaDetails = session.post(
            f'https://groups.roblox.com/v1/groups/{groupId}/users',


        ).json()['errors'][0]['fieldData']

        captchaId = captchaDetails.split('\",\"unifiedCaptchaId\":\"')[1].split('\"}"}]')[0].split('"}')[0]
        print(captchaId)
        captchaBlob = captchaDetails.split('"{\"dxBlob\":\"')[0].split('\",')[0].split('{"dxBlob":"')[1]
        print(captchaBlob)

        session.headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30',
            'origin':'https://www.roblox.com',
            'referer':'https://www.roblox.com/'
        }

        getToken = session.post(
            'https://roblox-api.arkoselabs.com/fc/gt2/public_key/63E4117F-E727-42B4-6DAA-C8448E9B137F',

            data = {
                'public_key':'63E4117F-E727-42B4-6DAA-C8448E9B137F',
                'userbrowser': session.headers['user-agent'],
                'rnd':f'0.{random.randint(1000,10000000)}',
                'data[blob]':captchaBlob,
                'language':'en'
            }
        ).json()['token']

    return {'token':getToken, 'captchaId':captchaId, 'captchaBlob':captchaBlob}

def join_group(cookie, groupId, captchaId, captchaToken):
    try:
        with requests.session() as session:
            session.cookies['.ROBLOSECURITY'] = cookie
            session.headers['x-csrf-token'] = session.post('https://friends.roblox.com/v1/users/1/request-friendship').headers['x-csrf-token']
            proxy = {}
            if config['settings'][0]['follow_bot']['proxies'] == True:
                __proxy_type__ = PROXY_TYPE
                proxy = {'http':f'{__proxy_type__}://{random.choice(proxies)}', 'https':f'{__proxy_type__}://{random.choice(proxies)}'}

            session.proxies = proxy

            follow = session.post(
                f'https://groups.roblox.com/v1/groups/{groupId}/users',

                data = {
                    'captchaId':captchaId,
                    'captchaToken':captchaToken,
                    'captchaProvider':'PROVIDER_ARKOSE_LABS'
                }
            )

            print(follow.text)

            if follow.status_code == 200:
                print(f'> Joined Group | {groupId} | {captchaId}')
            else:
                print(f'> Failed Join | {captchaId}')
    except:
        pass


def solve_captcha_group(token, captchaId, captchaBlob, cookie, GroupId):
    driver = autoselenium.Driver('edge')    
    location = token.split('|')[1]
    token_id = token.split('|')[0]
    solver_url = f'https://roblox-api.arkoselabs.com/fc/gc/?token={token_id}&{location}&lang=en&pk=A2A14B1D-1AF3-C791-9BBC-EE33CC7A0A6F&cdn_url=https%3A%2F%2Froblox-api.arkoselabs.com%2Fcdn%2Ffc'
    print(f'- Received Captcha Details!\n\n\nCaptchaId : {captchaId}\nCaptchaBlob : {captchaBlob}\nLocation : {location}\ntoken : {token_id}\n\n\n(Starting selenium browser to solve the captcha)..\n\n\n')
    driver.get(solver_url)
    time.sleep(3)
    print('\n\n[PRESS ENTER]: Press return/enter key on your keyboard if you finished the captcha!')
    input()
    driver.quit()
    threading.Thread(target=join_group, args=(cookie, GroupId, captchaId, token,)).start()

def select_group_join_bot():
    print('> Enter GroupId: ')
    group = input('-: ')
    print('\n\n> Started...')
    for x in cookies:
        try:
            captchaInfo = getCaptchaDetailsFromGroup(x, group)
            token = captchaInfo['token']
            captchaBlob = captchaInfo['captchaBlob']
            captchaId = captchaInfo['captchaId']
            solve_captcha_group(token, captchaId, captchaBlob, x, group)
        except:
            pass

    
    print('\n\n[FINISHED] > Press enter/return to go to the main screen!')
    input()
    return


def density_menu():
    print('>>> You are using [Density]: The ROBLOX purpose tool')
    print(f'>>> Loaded [{len(cookies)}] cookies / Loaded [{len(proxies)}] proxies\n')
    print(f'Developed by (rise#2636) discord.gg/8ysyfYmFJj')
    print('''
·▄▄▄▄  ▄▄▄ . ▐ ▄ .▄▄ · ▪  ▄▄▄▄▄ ▄· ▄▌
██▪ ██ ▀▄.▀·•█▌▐█▐█ ▀. ██ •██  ▐█▪██▌
▐█· ▐█▌▐▀▀▪▄▐█▐▐▌▄▀▀▀█▄▐█· ▐█.▪▐█▌▐█▪
██. ██ ▐█▄▄▌██▐█▌▐█▄▪▐█▐█▌ ▐█▌· ▐█▀·.
▀▀▀▀▀•  ▀▀▀ ▀▀ █▪ ▀▀▀▀ ▀▀▀ ▀▀▀   ▀ • 

1: Cookie Checker    4: Model Buyer   7: Friend Bot
2: Proxy Checker     5: Favorite Bot  8: Follow Bot
3: Cookie Generator  6: Visit Bot     9: Group Join 
    ''')
    selection = input('> ')
    features_list = [select_cookie_checker, select_proxy_checker, select_cookie_gen, select_model_bot, select_favorite_bot, select_visit_bot, select_friend_bot, select_follower_bot, select_group_join_bot]
    features_list[int(selection) -1]()
    global tasks
    tasks = 0
    os.system('cls')
    density_menu()


density_menu()


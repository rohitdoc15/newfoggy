from bardapi import BardCookies

cookie_dict = {
    "__Secure-1PSID": "cwjakILz6uWkpUwp56U3t5gJHR_mwfNKdS5dOlQ1WLMKYM1AiMRFNoLwEaJR2Jn5zc9W2g.",
    "__Secure-1PSIDTS": "sidts-CjEBNiGH7rnJwPtLKo9ppXlTVGrzTdVABaFrFuZbKdboBldUP0nT9JaEQxtepmnevqv4EAA",
    "__Secure-1PSIDCC": "ACA-OxMs7EpnzyHOjPqEoW7laTMBgy-aRFiQuvPwPTagwm0JnkeLRHpnQANWFGOoZ26EXhwxPA",
    # Any cookie values you want to pass session object.
}

bard = BardCookies(cookie_dict=cookie_dict)
print(bard.get_answer("""create a short blog on :

Uttarakhand | DGP Ashok Kumar tells ANI that heavy auger drilling machines have reached Chinyalisaur helipad for relief and rescue in Silkyara Tunnel of Uttarkashi district. These are being connected; drilling work will start soon. 

DGP has requested all the people to have patience and faith, soon all the workers will be rescued safely.""")['content'])
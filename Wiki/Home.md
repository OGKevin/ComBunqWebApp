<h3 align='center' >Welcome to the community bunq web app wiki!</h3>

<p align='center'>
<img src='http://in02.hostcontrol.com/resources/2f484a06146ef7/6cb30e544b.PNG'>
</p>
<p align='center'><i>Disclaimer: Bunq itself has nothing to do with this project.
<br>
This app is still in <a href='https://github.com/OGKevin/ComBunqWebApp/projects'>development</a>.
 </i></p>

---
This app will let bunqers handle their finances on a big screen. It will make use of the [bunq api] to get the user's data, non of this data is stored on this app's server, nor will the API key, installation token and private key.

This app is hosted on [heroku] and uses the included database. Currently the app is hosted on a free account, meaning that there are limitations more info about this can be found [here][heroku pricing].

---

## Resources

* [How to use](#how-to-use)
  * [Set up](#set-up)
  * [Buttons](#buttons)
    * [Buttons explained](#buttons-explained)
* [Examples](#examples)

---

## How to use

#### Set up
1. The app works with bunq's [exported CSV] or the [bunq api]. To make use of the [bunq api] you must create an account first. That can be done on the [registration page].

2. After creating an account you should generate an API key. From the bunq [website][API key]:

  <img src='https://www.bunq.com/files/pages/pages-api/security-nl.png' width=300>
  <img src='https://www.bunq.com/files/pages/pages-api/api-keys-nl.png' width=300>
  <img src='https://www.bunq.com/files/pages/pages-api/create-key-nl.png' width=300><br>
  
  ***Remember that bunq will charge for API usage, pricing can be found on page 8 & 9 of their [documentation][API price].***

3. After you have created your API key, you can [generate] an unique .json file that only you can use. To generate this file you must be logged in using 2 factor authentication. For security reasons please use a different password for encryption of this file.

    The file should look like this:
  
      ```json
  
      {
          "secret": "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",
          "userID": "e7f707bb-0bf9-4429-8a22-d91b08a74df2\r\n",
          "username": "OGKevin"
      }
      ```

4. Head over to the, for now called, [decrypt] page to register this device. Choice the generated .json file in step 3 and enter the password you've used to encrypt the secret. Load the file and press register.

5. Now you're ready to use the [bunq api]. Before you can start requesting your data from the bunq servers, you must start a session. From the bunq api [docs][bunq api docs]:

    >Sessions are temporary and expire after the same amount of time you have set for auto logout in your user account.

### Buttons

To get your data you can make use of the buttons porivede on the [decrypt] page. Each button will make an API call, even if you already have pressed the button before on the same session, this is because no data is getting stored.

##### Buttons explained

The buttons listed below are supported.

| Buttons | Explanation | Documentation |
|---------|-------------|---------------|
|Load file |  Lets javascript load the file so when a button is pressed the file contents can be send to the server. <br><br>Before an API call is made, the user ID from the file must match the one of the logged in user and the secret must be decrypted successfully.|- |
|Register|Registers the device(in this case the [Heroku] server) to your API.|https://doc.bunq.com/api/1/call/device-server |
| Start session | Starts a session (sort of loggin in) with the bunq servers. When a session is started an uniquely generated session token is send back, this token is then needed to make the data API calls.<br><br> This token is stored server side, even if an attackers gets this token it is useless without the decrypted secret which contains your API key. <br><br>When this call is made, the IP address used to make this call is locked to your API key. This will also return the users belonging to the API key, this will save you an API call. | https://doc.bunq.com/api/1/call/session-server |
| Users | Retrieves the users belonging to the API key. Each user has its own user ID. To get more details about a specific user, you should provide the user ID belonging to the user.| https://doc.bunq.com/api/1/call/user |
| Accounts | Retrieves the bank accounts belonging to the user. To make this call an user ID must be provided in the user ID box. Each account has its own account ID. To get more information about this account the account ID must be provided. | https://doc.bunq.com/api/1/call/monetary-account |
| Lock user & account ID | Like load file, when this button is pressed javascript will read the values entered in the user ID & account ID. These boxes can be empty.| - |
|Payment | Retrieves all the transactions belonging to an account. To use this button an user & account ID must be provided. | https://doc.bunq.com/api/1/call/payment |



---
## Examples

![example1]
![example2]
![example3]
![example4]

---

[bunq api]:<https://www.bunq.com/nl/api>
[heroku]:<https://www.heroku.com>
[heroku pricing]:<https://www.heroku.com/pricing>
[registration page]:<https://combunqweb.herokuapp.com/account/register/>
[API key]:<https://www.bunq.com/nl/api>
[API price]:<https://www.bunq.com/files/media/legal/en/20170310_Terms_bunq_API_EN_v1.1.pdf>
[generate]:<https://combunqweb.herokuapp.com/generate>
[decrypt]:<https://combunqweb.herokuapp.com/decrypt>
[bunq api docs]:<https://doc.bunq.com/api/1/page/introduction>
[example1]:<http://i.imgur.com/EN9XzYv.png>
[example2]:<http://i.imgur.com/jA1ZCOq.png>
[example3]:<http://i.imgur.com/MgYmjyD.png>
[example4]:<http://i.imgur.com/RoXnUg1.png>
[exported CSV]:<https://combunqweb.herokuapp.com/Manager/>

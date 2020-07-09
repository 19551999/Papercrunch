# PaperCrunch App Backend API Documentation

These are the APIs I wrote for an android tutorial application Papercrunch. The entire code is available on this repo.

## 1) User Registration API
    - endpoint  : /api/register/
    - request   : POST
    - headers   : None
    - HTTP Status Code Response :
        - 201 : When User Created
        - 400 : When any parameter missing or wrong
        - 405 : Empty Call
    - Input JSON parameters :
        - VARIABLE        DATA TYPE
        - email           String
        - password        String
        - first_name      Srting
        - last_name       String
        - avatarId        Integer (default = 0)
        - google          Boolean (Whether google Sign In or not)
    - Output JSON parameters :
        - VARIABLE        DATA TYPE
        - email           String
        - first_name      Srting
        - last_name       String
        - currentLevel    Integer (default = 1)
        - totalStars      Integer (default = 0)
        - avatarId        Integer (default = 0)
        - google          Boolean (Whether google Sign In or not)
    - Input Example:
        {
            "email": "test@test.com",
            "password" : "12345678",
            "first_name": "Test",
            "last_name": "User",
            "avatarId": 2,
            "google": False
        }
    - Output Example:
        {
            "email": "test@test.com",
            "first_name": "Test",
            "last_name": "User",
            "currentLevel": 1,
            "totalStars": 0,
            "avatarId": 2,
            "google": False
        }


## 2) User Login API
    - endpoint  : /api/login/
    - request   : POST
    - headers   : None
    - HTTP Status Code Response :
        - 200 : When Passed
        - 400 : When any parameter missing or wrong
        - 405 : Empty Call
    - Input JSON parameters :   
        - VARIABLE    DATA TYPE
        - email       String
        - password    String
    - Output JSON parameters :
        - VARIABLE      DATA TYPE
        - token         String
        - currentLevel  Integer = currentLevel Primary Key last synced
        - totalStars    Integer = Last synced
        - badges        Integer = Last synced
    - Input Example :
        {
            "email": "test@test.com",
            "password" : "12345678"
        }
    - Output Example :
        {
            "token": "30fc71ae2bf5af28c6913e6d237c3cdf34a6fffb",
            "currentLevel": 1,
            "totalStars": 0,
            "avatarId": 0
        }


## 3) Reset Password API
    - endpoint  : /api/reset-password/
    - request   : POST
    - headers   : None
    - HTTP Status Code Response :
        - 200 : When Passed
        - 400 : When any parameter missing or wrong
        - 405 : Empty Call
    - Input JSON parameters :
        - NAME   DATA TYPE
        - email  String 
    - Input Example:
        {
            "email": "test@test.com"
        }


## 4) Change Password API
    - endpoint  : /api/change-password/
    - request   : POST
    - headers   : Authorization - Token required (Provided during Login)
    - HTTP Status Code Response :
        - 201 : When Passed
        - 400 : When any parameter missing or wrong or wrong (Not Sure)
        - 401 : Unauthorized request
    - Input JSON parameters :
        - NAME         DATA TYPE
        - password     String
        - new_password String                          
    - Input Example:
        {
            "password": "12345678",
            "new_password": "87654321"
        }


## 5) Sync Data From Mobile API
    - endpoint  : /api/sync-from-mobile/
    - request   : POST
    - headers   : Authorization - Token required (Provided during Login)
        - HTTP Status Code Response :
        - 201 : When Passed
        - 400 : When any parameter missing or wrong
        - 401 : Unauthorized request
    - Input JSON parameters :
        - NAME         DATA TYPE
        - currentLevel Integer (currentLevel Primary Key)
        - totalStars   Integer 
        - avatarId     Integer (0-8) 
    - Input Example :
        {
            "currentLevel": 2,
            "totalStars": 6,
            "avatarId": 2
        }


## 6) Sub Level Status API
    - endpoint  : /api/status/
    - request   : GET, POST
    - headers   : Authorization - Token required (Provided during Login)
    - HTTP Status Code Response :
        - 200 : When GET request is successful
        - 201 : When POST request is successful
        - 400 : When user doesn't exist
        - 401 : Unauthorized request
    - GET request :
        - Response :
            {
                "subLevel1": 0,
                "subLevel2": 0,
                "subLevel3": 0,
                "subLevel4": 0,
                "subLevel5": 0,
                "subLevel6": 0,
                "subLevel7": 0,
                "subLevel8": 0,
                "subLevel9": 0,
                "subLevel10": 0,
                "subLevel11": 0,
                "subLevel12": 0,
                "subLevel13": 0,
                "subLevel14": 0,
                "subLevel15": 0,
                "subLevel16": 0,
                "subLevel17": 0,
                "subLevel18": 0,
                "subLevel19": 0,
                "subLevel20": 0,
                "subLevel21": 0,
                "subLevel22": 0,
                "subLevel23": 0,
                "subLevel24": 0,
                "subLevel25": 0,
                "subLevel26": 0,
                "subLevel27": 0
            }
    - POST request :
        - Request :
            {
                "subLevel1": 2,
                "subLevel2": 2,
                "subLevel3": 2,
                "subLevel4": 2,
                "subLevel5": 2,
                "subLevel6": 2,
                "subLevel7": 1,
                "subLevel8": 1,
                "subLevel9": 1,
                "subLevel10": 1,
                "subLevel11": 1,
                "subLevel12": 1,
                "subLevel13": 1,
                "subLevel14": 1,
                "subLevel15": 0,
                "subLevel16": 0,
                "subLevel17": 0,
                "subLevel18": 0,
                "subLevel19": 0,
                "subLevel20": 0,
                "subLevel21": 0,
                "subLevel22": 0,
                "subLevel23": 0,
                "subLevel24": 0,
                "subLevel25": 0,
                "subLevel26": 0,
                "subLevel27": 0
            }
    


## 7) Level Progress API
    - endpoint  : /api/user-progress/
    - request   : POST
    - headers   : Authorization - Token required (Provided during Login)
    - HTTP Status Code Response :
        - 200 : When GET request is successful
        - 201 : When POST request is successful
        - 400 : When user doesn't exist
        - 401 : Unauthorized request
    - GET request :
        - Response :
            {
                "levelOne" : 100,
                "levelTwo" : 90,
                "levelThree" : 80,
                "levelFour" : 95,
                "levelFive" : 0,
                "levelSix" : 0,
                "levelSeven" : 0,
                "levelEight" : 0,
                "levelNine" : 0
            }
    - POST request :
        - Request :
            {
                "levelOne" : 100,
                "levelTwo" : 90,
                "levelThree" : 80,
                "levelFour" : 95,
                "levelFive" : 0,
                "levelSix" : 0,
                "levelSeven" : 0,
                "levelEight" : 0,
                "levelNine" : 0
            }


## 8) Sync Data To Mobile API
### i) Levels Database
        - endpoint  : /api/levels/
        - request   : GET
        - headers   : Authorization - Token required (Provided during Login)
        - HTTP Status Code Response :
            - 200 : Successful request
            - 401 : Unauthorized request
        - Output JSON parameters :
            - NAME       DATA TYPE
            - levelName  String
        - Output Example :
            [
                {
                    "levelName": "Introduction"
                },
                {
                    "levelName": "Data Types and Variables"
                },
            ]

### ii) Sub Levels Concepts Database
        - endpoint  : /api/sub-level-concepts/
        - request   : GET
        - headers   : Authorization - Token required (Provided during Login)
        - HTTP Status Code Response :
            - 200 : Successful request
            - 401 : Unauthorized request
        - Output JSON parameters :                        
            - NAME         : DATA TYPE
            - conceptText  : Text
            - level        : Integer (Which Level it belongs to)
            - sublevelName : String
        - Output Example :
            [
                {
                    "conceptTextOne": "Test",
                    "conceptTextTwo": "Test",
                    "conceptTextThree": "Test",
                    "level": 1,
                    "subLevelName": "What is Programming?"
                },
                {
                    "conceptTextOne": "Test",
                    "conceptTextTwo": "Test",
                    "conceptTextThree": "Test",
                    "level": 1,
                    "subLevelName": "What is C?"
                },
                {
                    "conceptTextOne": "Test",
                    "conceptTextTwo": "Test",
                    "conceptTextThree": "Test",
                    "level": 1,
                    "subLevelName": "Basic C Program Syntax"
                }
            ]

### iii) Sub Levels Quiz Database
        - endpoint  : /api/sub-level-quiz/
        - request   : GET
        - headers   : Authorization - Token required (Provided during Login)
        - HTTP Status Code Response :
            - 200 : Successful request
            - 401 : Unauthorized request
        - Output JSON parameters :
            - NAME         : DATA TYPE
            - answer     : Text (String)
            - hint       : Text (String)
            - optionOne  : Text (String)
            - optionThree: Text (String)
            - optionTwo  : Text (String)
            - question   : Text (String)
            - stars      : Integer (How many stars for the question, like max marks)
            - subLevel   : Integer (Primary Key of the Sub Level Concepts it is quiz question to)
        - Output Example :
            [
                {
                    "answer": "Option 3",
                    "hint": "Test Hint",
                    "optionOne": "Option 1",
                    "optionThree": "Option 3",
                    "optionTwo": "Option 2",
                    "question": "Test Question",
                    "stars": 3,
                    "subLevel": 2
                }
            ]


## 9) Playground API
    - endpoint : /api/playground/
    - request  : POST
    - headers  : Authorization - Token required (Provided during Login)
    - HTTP Status Code Response :
        - 200 : When Passed
        - 401 : Unauthorized request
    - Input JSON parameters :
        - NAME  DATA TYPE
        - code  Text (Whole Code)                            
    - Output JSON parameters :
        NAME            DATA TYPE
        compiled_result Text
        run_result      Text
    - Input Example :
            {
                "code":"#include<stdio.h> int
                        int main() {
                            printf("Hello World");
                            return(0);
                        }",
            }
    - Output Example :
            {
                "compiled_result":"",
                "run_result":"Hello World"
            }


## 10) Logout API
    - endpoint : /api/logout/
    - request  : GET
    - headers  : Authorization - Token required (Provided during Login)
    - HTTP Status Code Response :
        - 200 : When Passed
        - 401 : Unauthorized request


## 11) Google Sign In Check API
    - endpoint : /api/google-sign-in-check/
    - request  : POST
    - headers  : None
    - HTTP Status Code Response :
        - 200 : When Passed
        - 400 : When any parameter missing or wrong
    - Input JSON parameters :
        - NAME  : DATA TYPE
        - email : String
    - Output JSON parameters :
        - NAME   : DATA TYPE
        - google : Boolean
        - exists : Boolean
    - Input Example:
        {
            "email": "test@test.com"
        }
    - Output Example:
        {
            "google": false,
            "exists": true
        }

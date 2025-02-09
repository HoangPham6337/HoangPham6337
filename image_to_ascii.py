import os
import urllib.request
from ascii_magic import AsciiArt
from get_user_data import fetch_user_data

def convert_picture_to_ascii(columns: int) -> str:
    # avatar_url: str =  str(fetch_user_data(os.environ["USER_NAME"])["avatar_url"])
    # urllib.request.urlretrieve(avatar_url, "avatar.jpg")
    # avatar_art = AsciiArt.from_image("avatar.jpg")
    # return avatar_art.to_ascii(columns=columns, monochrome=True)
    return """                                                  
                                                  
                                                  
                                                  
                    ........                      
                ..::--=====--:. .........         
              ..:-::::::----------=------:..      
             ..---=------::::::::::::::::-:.      
          ..-----::::::::::::::--::::::::-:.      
       .---::::::::--=+=========+-----::-:..      
     .=:::::::-=+==========-----++-:::--..        
     --::::======-...:---------....--...          
      :-:::::=--:..::::------=:..=--..=:..        
            .----.....--------=:..::.--.::.       
            :------=-----=========-..=..:..       
           .=------=--:::::::::::--.=...:.        
           .=--------:::::::::::--.-:..:-..       
           .==-----+==-:::::::::-==+:. .-++.      
           .=------===-:::::::::-:-:. ..=++-.     
           .=--------::::::::::---:.. ..-=+:.     
           .:=----++==-::::::------:.   .-+:.     
             .::-====::---:::..:::..    ....      
               ...... .....                       
                                                  
                                                  
                                                  
                                                  
    """

if __name__ == "__main__":
    print(convert_picture_to_ascii(100))
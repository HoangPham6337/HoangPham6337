def convert_picture_to_ascii(columns: int) -> str:
    # avatar_url: str =  str(fetch_user_data(os.environ["USER_NAME"])["avatar_url"])
    # urllib.request.urlretrieve(avatar_url, "avatar.jpg")
    # avatar_art = AsciiArt.from_image("avatar.jpg")
    # return avatar_art.to_ascii(columns=columns, monochrome=True)
    return """                                                                        
                                                                        
                                                                        
                                                                        
                                                                    
                                                                    
                                                                    
                          ...::--=====--:..                         
                        .:==:::::::::::::-=:. ............          
                     ..-=:::::::::::---=======---::::::::-=-..      
                     .=:::---======--::::::::::::::::-:::::-=.      
                 ....+====--:::::::::::-::::::-:::::--::::::=:      
               .:-=-::::::::::::-:::::::::---------:-:::::::=.      
          ..:==::-::::::--::::--=++++=========+------=-::::=..      
       ..:=-:-::::::::::-=++================---+---::::::-=.        
       .=-:::::::::-=++=============--------==:::=-:::-=-..         
       .+:::::::=+======+-.....-=----------+:......+-:.             
       ..=-::::::::=---+........:=----------...:==:-: .-:..         
          ..---:...----=...=**=..+---------=.......=. :+.:-.        
                 ..----+:.......-=----=-=---=.....-...+:...-        
                 .=-----==.....=--------------====:..--...::        
                 .=---------=====++====-----::---=:.:+. .:-.        
                .:-------------::::::::::::::::--=..=.  .-.         
                .--=-----------::::::::::::::::-+..==.  .-.         
                .==-----------:::::::::::::::::-===*:   ..:-::.     
                .===--------=+=+-:::::::::::::-+==++.    .=+++.     
                .==--------==-===:::::::::::::--.-=..   .:++++-.    
                .=-----------==::::::::::::::--=.-..    .+++++=.    
                .-------------:::::::::::::::-=++=:.    ...-++:.    
                 .==------+=+++=::::::::::::-----=-.       -++-.    
                 ...===-------==-:::::--==::-====:..       :....    
                      ..:-===- ........                             
                                                                    
                                                                    
                                                                    
     ___  ___  ________  ________ ________  ________   ________     
     |\  \|\  \|\   __  \|\   ____\\_____  \|\_____  \ |\_____  \   
     \ \  \\\  \ \  \|\  \ \  \___\|____|\ /\|____|\ /_ \|___/  /|  
      \ \   __  \ \   ____\ \  \____    \|\  \    \|\  \    /  / /  
       \ \  \ \  \ \  \___|\ \  ___  \ __\_\  \  __\_\  \  /  / /   
        \ \__\ \__\ \__\    \ \_______\\_______\|\_______\/__/ /    
         \|__|\|__|\|__|     \|_______\|_______|\|_______||__|/     
                                                                    
                                                                    
                                                                    
                                                                    """

if __name__ == "__main__":
    print(convert_picture_to_ascii(100))

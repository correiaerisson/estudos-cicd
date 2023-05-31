import vlc

instance = vlc.Instance()
media_ply = instance.media_player_new()
media_ply.set_mrl("teste.mp3")
media_ply.play()

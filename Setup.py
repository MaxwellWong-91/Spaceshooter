import cx_Freeze

executables = [cx_Freeze.Executable("SpaceShooter.py")]

cx_Freeze.setup(
    name = "SpaceShooter",
    options = {"build_exe": {"packages":["pygame", "os", "sys", "math", "random"],
                             "include_files": [("Player.py", "Player.py"), 
                                               ("Enemy.py", "Enemy.py"), ("Bullet.py", "Bullet.py"), ("Background Music.mp3", "Background Music.mp3"),
                                               ("Images\Background\game_background_4.png", "Images\Background\game_background_4.png"), 
                                               (r"Images\Blue\Animation\B1.png", r"Images\Blue\Animation\B1.png"),
                                               (r"Images\Blue\Animation\B2.png", r"Images\Blue\Animation\B2.png"),
                                               (r"Images\Blue\Animation\B3.png", r"Images\Blue\Animation\B3.png"),
                                               (r"Images\Blue\Animation\B4.png", r"Images\Blue\Animation\B4.png"),
                                               (r"Images\Blue\Animation\B5.png", r"Images\Blue\Animation\B5.png"),
                                               (r"Images\Blue\Animation\B6.png", r"Images\Blue\Animation\B6.png"),
                                               (r"Images\Blue\Animation\B7.png", r"Images\Blue\Animation\B7.png"),
                                               (r"Images\Blue\Animation\B8.png", r"Images\Blue\Animation\B8.png"),
                                               (r"Images\Red\small_ship_animation\R1.png", r"Images\Red\small_ship_animation\R1.png"),
                                               (r"Images\Red\small_ship_animation\R2.png", r"Images\Red\small_ship_animation\R2.png"),
                                               (r"Images\Red\small_ship_animation\R3.png", r"Images\Red\small_ship_animation\R3.png"),
                                               (r"Images\Red\small_ship_animation\R4.png", r"Images\Red\small_ship_animation\R4.png"),
                                               (r"Images\Red\small_ship_animation\R5.png", r"Images\Red\small_ship_animation\R5.png"),
                                               (r"Images\Blue\bullet_copy.png", r"Images\Blue\bullet_copy.png"),
                                               (r"Images\Red\bullet_red.png", r"Images\Red\bullet_red.png") ] }},
    executables = executables
                )


python3.12.5:
C:\Users\imsve\AppData\Local\Programs\Python\Python312\python.exe -m pip install socketify

changed C:\intern\xtts-2\server\TTS\utils\synthesizer.py line 252 +255 
changed C:\intern\xtts-2\server\TTS\api.py line 344

C:\Users\imsve\.dstack\server\config.yml

run dstack.yaml with "dstack run run-on-vastai"

{
  "Arabic": "ar",
  "Chinese": "zh-cn",
  "Czech": "cs",
  "Dutch": "nl",
  "English": "en",
  "French": "fr",
  "German": "de",
  "Hungarian": "hu",
  "Italian": "it",
  "Japanese": "ja",
  "Korean": "ko",
  "Polish": "pl",
  "Portuguese": "pt",
  "Russian": "ru",
  "Spanish": "es",
  "Turkish": "tr"
}



data for testing:

C:\intern\xtts-2\voice_samples\Usachev 10.mp3
    C:\intern\xtts-2\voice_samples\woman.mp3
    C:\intern\xtts-2\voice_samples\Faib 10.mp3
    
    C:\intern\xtts-2\voice_samples\Usachev 10.wav

    path_to_save_file = r'C:\intern\xtts-2\res\en'

    The cat jumped swiftly onto the wooden windowsill.
    She picked up her book and settled into the cozy chair.
    He smiled as he watched the children play in the park.
    Hello, this is a test. 
    The sun set behind the hills, casting a warm glow across the sky. The day slowly turned into night, and the stars began to appear, twinkling softly as the world around them quieted down for rest.

    Осенний вечер принес прохладу и легкий ветерок, листья мягко кружатся в воздухе, создавая атмосферу уюта. В домах загораются теплые огни, а люди наслаждаются спокойствием уходящего дня.
    Солнце скрылось за горами, окрашивая небо в оранжевый.
    Он улыбался, наблюдая за детьми, играющими в парке.

    Il sourit en regardant les enfants jouer dans le parc.
    Le soleil se couche, illuminant l'horizon rouge.
    En plein cœur de l'automne, les arbres se parent de teintes orangées et rouges. Le vent souffle doucement, emportant avec lui les feuilles mortes qui tourbillonnent avant de toucher le sol humide.

    sentences_en = [
        # English
        "The sun sets so fast.",
        "He loves coding daily.",
        "She read a new book.",
        "The stars twinkle bright.",
        "Time flies when happy."]
    
    sentences_ru_not_dot = [
        # Russian
        "Солнце садится быстро",
        "Он любит кодить каждый день",
        "Она прочитала новую книгу",
        "Звезды ярко мерцают",
        "Время летит, когда счастлив"]

    sentences_fr = [
        # French
        "Le soleil se couche vite.",
        "Il aime coder tous les jours.",
        "Elle a lu un nouveau livre.",
        "Les étoiles brillent fort.",
        "Le temps passe vite quand on est heureux."
    ]

    texts_en = [
        # English
        "The sun was setting over the horizon, casting a golden glow. Birds sang, filling the air with calm.",
        "In the busy city, life moved quickly. People rushed through the streets, deep in their own thoughts.",
        "On a quiet evening, a soft breeze rustled the leaves. It was the perfect moment for peace and reflection."]
    texts_fr = [
        # French
        "Le soleil se couchait à l'horizon, projetant une lueur dorée. Les oiseaux chantaient, remplissant l'air de calme.",
        "Dans la ville animée, la vie avançait rapidement. Les gens se précipitaient dans les rues, perdus dans leurs pensées.",
        "Par une soirée tranquille, une douce brise faisait bruisser les feuilles. C'était le moment parfait pour la paix et la réflexion."]
    texts_sp = [
        # Spanish
        "El sol se ponía en el horizonte, proyectando un brillo dorado. Los pájaros cantaban, llenando el aire de calma.",
        "En la ciudad ocupada, la vida se movía rápido. La gente se apresuraba por las calles, sumida en sus propios pensamientos.",
        "En una tarde tranquila, una suave brisa movía las hojas. Era el momento perfecto para la paz y la reflexión."]
    texts_ru = [
        # Russian
        "Солнце садилось за горизонт, отбрасывая золотой свет. Птицы пели, наполняя воздух покоем.",
        "В шумном городе жизнь текла быстро. Люди спешили по улицам, погруженные в свои мысли.",
        "Тихим вечером мягкий ветерок шелестел листьями. Это был идеальный момент для мира и размышлений."
    ]



    short_sentences_en = [
        # English
        "I'm so sad.",  
        "I'm so mad!",  
        "How funny!",   
        "I'm afraid.",  
        "So peaceful."]
    short_sentences_ru = [
        # Russian
        "Мне так грустно.",  
        "Я в ярости!",       
        "Как смешно!",       
        "Я боюсь.",          
        "Так спокойно."]
    
    short_sentences_fr = [
        # French
        "Je suis triste.",    
        "Je suis furieux!",   
        "C'est drôle!",       
        "J'ai peur.",         
        "Si paisible."]
    short_sentences_es = [
        # Spanish
        "Estoy triste.",      
        "¡Estoy furioso!",    
        "¡Qué gracioso!",     
        "Tengo miedo.",       
        "Tan tranquilo.",     
    ]



    big_text_en = "The sun was setting over the horizon, painting the sky with hues of orange and pink. The gentle breeze carried the scent of the ocean, and the waves softly lapped against the shore. It was the perfect evening, one that seemed to hold infinite possibilities. As the first stars appeared, a sense of peace washed over me, and I realized that sometimes, the simplest moments can bring the greatest joy. Life felt calm and meaningful in that quiet, serene twilight."
    big_text_ru = "Солнце заходило за горизонт, окрашивая небо в оттенки оранжевого и розового. Лёгкий ветерок приносил аромат моря, а волны мягко омывали берег. Это был идеальный вечер, казалось, он хранил в себе бесконечные возможности. Когда появились первые звезды, на меня нахлынуло чувство умиротворения, и я осознал, что иногда самые простые моменты могут принести наибольшую радость. Жизнь казалась спокойной и значимой в этом тихом, безмятежном сумраке." 


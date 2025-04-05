**Alla peab laetud olema git

1. Loo endale kaust

2. Ava cmd ning kirjuta: cd sinuKaust

3. kirjuta: git clone https://github.com/Astonnnn/Kvalifikatsioon

4. Loo ja Aktiveeri virtuaalne keskkond 

   4.1 python -m venv env

   4.2 env\Scripts\activate

    Asi on õnnestunud, kui cmd's on su kausta nime ees (env)    

3. Lae alla moodulid

    3.1 pip install -r requirements.txt
    
    Asi on õnnestunud, kui sinu kausta, kui sa vaatad kas file explorerist
    või mujalt kaustas env, selle alamkaustas Scripts mitmed erinevad .exe failid

4. Ühenda enda kaust gihubiga, kui pole juba

    git remote remove origin

    git remote add origin "https://github.com/Astonnnn/Kvalifikatsioon"
    


ÜLES LAADIMINE

1. git status (kontrollime, millised failid muutusid)
2. git add . (lisame kõik muutused valikusse)
3. git commit -m "Kirjeldus" (Commitime koos kommetaariga)
4. git push origin main
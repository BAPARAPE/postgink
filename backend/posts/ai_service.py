import os
from groq import Groq

client = Groq(api_key=os.getenv('GROQ_API_KEY'))


def generate_post(subject, tone, job_title, industry, interests):
    tone_descriptions = {
        'professional': 'professionnel et expert, avec des insights pertinents',
        'storytelling': 'narratif et personnel, avec une histoire engageante',
        'hot_take': 'direct et provocateur, avec une opinion tranchée',
    }

    prompt = f"""Tu es un expert en personal branding LinkedIn pour les professionnels de la tech.

Génère un post LinkedIn en français pour cette personne :
- Métier : {job_title}
- Secteur : {industry}
- Intérêts : {interests}

Sujet du post : {subject}
Ton souhaité : {tone_descriptions.get(tone, 'professionnel')}

Règles importantes :
- Entre 150 et 300 mots
- Commence par une accroche forte qui donne envie de lire
- Utilise des sauts de ligne pour aérer le texte
- Termine par une question ou un call-to-action pour engager
- Maximum 3-5 hashtags à la fin
- Écris uniquement le contenu du post, rien d'autre"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000
    )

    return response.choices[0].message.content


def suggest_subjects(job_title, industry, interests):
    prompt = f"""Tu es un expert en personal branding LinkedIn pour les professionnels de la tech.

Propose 5 sujets de posts LinkedIn pertinents et engageants pour cette personne :
- Métier : {job_title}
- Secteur : {industry}
- Intérêts : {interests}

Règles :
- Chaque sujet doit être accrocheur et spécifique
- Variés : tips pratiques, retour d'expérience, opinion, tendance, carrière
- Entre 10 et 20 mots par sujet
- Réponds UNIQUEMENT avec une liste JSON de 5 strings, rien d'autre

Format attendu :
["sujet 1", "sujet 2", "sujet 3", "sujet 4", "sujet 5"]"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )

    import json
    subjects = json.loads(response.choices[0].message.content)
    return subjects
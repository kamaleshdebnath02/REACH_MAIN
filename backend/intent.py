import spacy

# Load the English NLP model
nlp = spacy.load('en_core_web_sm')


def extract_main_topic(text):
    """ Extract the main health-related topic from the text, covering a wide range of topics and understanding grammatical context """
    doc = nlp(text)
    
    # Comprehensive list of health-related keywords covering various categories
    health_related_keywords = {
        # Common diseases and conditions in rural areas
        'disease', 'condition', 'symptom', 'health issue', 'jaundice', 'fever', 'cold', 
        'flu', 'diabetes', 'hypertension', 'cancer', 'asthma', 'arthritis', 
        'migraine', 'headache', 'fatigue', 'allergy', 'infection', 'covid-19',
        'malaria', 'typhoid', 'cholera', 'tuberculosis', 'measles', 'chickenpox',
        'dengue', 'leprosy', 'filariasis', 'pneumonia', 'hepatitis', 'HIV', 'AIDS',
        'rabies', 'anemia', 'malnutrition', 'dehydration', 'worms', 'gastroenteritis',
        'heat stroke', 'sunburn', 'hypothermia', 'scabies', 'ringworm', 'intestinal infections',
        'kala-azar', 'guinea worm', 'polio', 'elephantiasis', 'trachoma', 'meningitis',
        'diphtheria', 'whooping cough', 'dysentery', 'brucellosis', 'typhus', 'yellow fever',

        # Traditional health practices and local remedies
        'ayurveda', 'home remedies', 'natural remedies', 'herbal medicine', 'yoga',
        'meditation', 'tulsi', 'neem', 'turmeric', 'ashwagandha', 'aloe vera',
        'ginger', 'garlic', 'honey', 'cinnamon', 'fenugreek', 'amla', 'bhrami',
        'siddha', 'unani', 'acupuncture', 'acupressure', 'naturopathy', 'herbal teas',
        'panchakarma', 'chiropractic', 'aromatherapy', 'massage therapy', 'reiki',
        'naturopathy', 'holistic health', 'traditional healing practices', 'folk medicine',

        # Diet and nutrition
        'balanced diet', 'malnutrition', 'vitamin deficiencies', 'protein-energy malnutrition',
        'staple foods', 'grains', 'pulses', 'seasonal vegetables', 'seasonal fruits',
        'millet', 'sorghum', 'rice', 'wheat', 'maize', 'lentils','healthy', 'local diet practices',
        'cooking methods', 'food preservation', 'fermented foods', 'nutritional habits',
        'child nutrition', 'dietary diversity', 'food security', 'food fortification',

        # Sanitation and hygiene
        'sanitation', 'clean water', 'hygiene', 'toilet facilities',
        'open defecation', 'waterborne diseases', 'handwashing', 'bathing practices',
        'waste disposal', 'community health', 'rural health infrastructure',
        'water purification', 'personal hygiene', 'sanitary practices', 'cleanliness',
        'environmental sanitation', 'sewage management', 'wastewater treatment',

        # Maternal and child health
        'maternal health', 'child health', 'antenatal care', 'postnatal care',
        'immunization', 'childhood vaccines', 'breastfeeding', 'infant nutrition',
        'midwifery', 'birth attendants', 'traditional birth practices',
        'safe motherhood', 'family planning', 'newborn care', 'growth monitoring',
        'child development', 'maternal nutrition', 'high-risk pregnancies',

        # Miscellaneous health topics relevant to rural settings
        'first aid', 'snake bites', 'animal bites', 'injury care', 'fractures',
        'burns', 'falls', 'occupational hazards', 'pesticide exposure', 'respiratory issues',
        'seasonal ailments', 'monsoon diseases', 'summer ailments', 'winter ailments',
        'community health workers', 'ASHA workers', 'mobile health units', 'telemedicine',
        'health camps', 'rural outreach', 'public health initiatives', 'health education',
        'nutrition programs', 'water sanitation and hygiene (WASH)', 'vector control',

        # Chronic diseases and long-term conditions
        'chronic disease', 'chronic pain', 'heart disease', 'stroke', 'cholesterol', 
        'blood pressure', 'cardiovascular health', 'respiratory health', 'diabetes management',
        'insulin resistance', 'thyroid', 'autoimmune disease', 'liver health', 'kidney health',
        'COPD', 'arthritis', 'osteoporosis', 'Alzheimer’s', 'Parkinson’s', 'fibromyalgia',
        'cataracts', 'glaucoma', 'dementia', 'epilepsy', 'cystic fibrosis', 'sickle cell anemia',
        'thalassemia', 'asbestosis', 'silicosis', 'chronic fatigue syndrome', 'varicose veins',

        # Lifestyle and preventive health
        'healthy lifestyle', 'preventive health', 'healthy aging', 'lifestyle changes', 
        'smoking cessation', 'alcohol moderation', 'substance abuse', 'drug addiction',
        'physical activity', 'workout routine', 'sleep hygiene', 'nutritional balance',
        'screen time', 'digital detox', 'mindful eating', 'clean eating', 'sustainable living',
        'mental well-being', 'stress management', 'positive mental health', 'resilience',
        'community support', 'social health', 'behavioral health', 'preventive care',
        'health screening', 'early detection', 'disease prevention', 'health promotion',

        # Miscellaneous Health Topics
        'hydration', 'sun protection', 'UV exposure', 'radiation', 'toxins', 
        'air quality', 'pollution', 'environmental health', 'occupational health',
        'ergonomics', 'injury prevention', 'vaccines', 'disease prevention',
        'first aid', 'CPR', 'burn care', 'wound care', 'fractures', 'sprains',
        'immune system', 'antioxidants', 'inflammation', 'detox drinks', 'superfoods',
        'food safety', 'contaminated food', 'foodborne illnesses', 'malaria prevention',
        'personal protective equipment (PPE)', 'occupational safety', 'accident prevention',
        'workplace hazards', 'industrial safety', 'agricultural safety', 'child labor risks',
        'nutrition supplementation', 'community kitchens', 'anganwadi services', 'rural nutrition schemes'
    }

    # Check for known health-related keywords in the text
    for token in doc:
        if token.lemma_ in health_related_keywords:
            return token.text

    # Use named entities recognized by spaCy if they match specific categories
    for ent in doc.ents:
        if ent.label_ in ['DISEASE', 'SYMPTOM', 'HEALTH_CONDITION', 'VITAMIN', 'DIET', 'NUTRITION', 'EXERCISE']:
            return ent.text

    # Use noun chunks to find relevant health-related topics
    noun_chunks = [chunk.text for chunk in doc.noun_chunks if chunk.text.lower() not in {'i', 'you', 'he', 'she', 'it', 'we', 'they'}]

    # Analyze noun chunks for specific health-related contexts
    for chunk in noun_chunks:
        chunk_doc = nlp(chunk)
        for token in chunk_doc:
            if token.dep_ in {'nsubj', 'dobj', 'pobj', 'attr'} and token.lemma_ in health_related_keywords:
                return chunk

    # Analyze the grammatical structure of the text for main topics
    main_topics = []
    for token in doc:
        if token.dep_ in {'nsubj', 'dobj', 'pobj', 'attr'}:
            if token.lemma_ in health_related_keywords:
                main_topics.append(token.text)
            else:
                # Look for compound nouns or proper nouns that might represent a main topic
                compound_noun = ' '.join([child.text for child in token.children if child.dep_ == 'compound'])
                if compound_noun:
                    main_topics.append(compound_noun + ' ' + token.text)
    
    # Return the most likely main topic
    if main_topics:
        return max(set(main_topics), key=main_topics.count)

    # Fallback to the first noun chunk if no specific health-related keyword is found
    if noun_chunks:
        return noun_chunks[0]

    return None

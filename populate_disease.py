import pandas as pd
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://plantcare_user:1234@localhost/organic_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Disease(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    disease_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    organic_solution = db.Column(db.Text)
    guidance = db.Column(db.Text)
    possible_steps = db.Column(db.Text)

# Updated CSV data with detailed descriptions and Tamil Nadu-specific organic solutions
csv_data = [
    {
        "index": 0,
        "disease_name": "Apple___Apple_scab",
        "description": "Apple scab, caused by the fungus *Venturia inaequalis*, manifests as dark, velvety spots on leaves, often turning black or brown. It affects leaves, fruit, and twigs, leading to reduced photosynthesis and fruit quality. The disease thrives in cool, wet conditions, common during spring in Tamil Nadu.",
        "Possible Steps": "Choose resistant varieties and avoid overhead irrigation.",
        "Organic_Solution": "Prepare Panchagavya by mixing 5 kg fresh cow dung, 3 L cow urine, 2 L cow milk, 2 L curd, 1 kg ghee, 1 kg jaggery, 3 ripe bananas, and 1 L tender coconut water. Ferment for 7 days, stirring daily. Dilute 3 L Panchagavya in 100 L water and spray biweekly. Alternatively, apply 20 kg fermented cow dung compost per hectare monthly to improve soil health and suppress fungal spores.",
        "Guidance": "Prune trees to improve air circulation. Remove fallen leaves to reduce fungal spores."
    },
    {
        "index": 1,
        "disease_name": "Apple___Black_rot",
        "description": "Black rot, caused by the fungus *Botryosphaeria obtusa*, results in blackened, shriveled fruit and dark lesions on leaves and twigs. It can cause significant yield loss and is prevalent in warm, humid conditions.",
        "Possible Steps": "Remove cankers and infected fruit.",
        "Organic_Solution": "Prepare a garlic extract by blending 100 g garlic with 1 L water, strain, and dilute with 10 L water. Add 50 ml neem oil and spray weekly. Alternatively, apply 5 L Amrit Jal (mix 10 kg cow dung, 5 L cow urine, 1 kg jaggery, ferment for 3 days) per hectare as a soil drench to enhance plant immunity.",
        "Guidance": "Sanitize tools after use to prevent spread."
    },
    {
        "index": 2,
        "disease_name": "Apple___Cedar_apple_rust",
        "description": "Cedar apple rust, caused by the fungus *Gymnosporangium juniperi-virginianae*, produces yellow-orange spots on leaves, often with black centers, and can affect fruit. It requires cedar trees as an alternate host and thrives in wet, warm weather.",
        "Possible Steps": "Remove nearby cedar trees.",
        "Organic_Solution": "Mix 5 kg wood ash with 100 L water and spray as a foliar application every 10 days to control fungal growth. Combine with 3 L Panchagavya diluted in 100 L water for enhanced effect. Apply 10 kg neem cake per hectare to soil to deter fungal spores.",
        "Guidance": "Monitor for rust galls on cedar trees."
    },
    {
        "index": 3,
        "disease_name": "Apple___healthy",
        "description": "Healthy apple plants exhibit vibrant green leaves, strong stems, and blemish-free fruit. Regular care prevents disease onset.",
        "Possible Steps": "Maintain regular care.",
        "Organic_Solution": "Apply 500 kg well-decomposed cow dung compost per hectare every 3 months to enrich soil. Spray 3 L Jeevamrutham (mix 10 kg cow dung, 10 L cow urine, 2 kg jaggery, 2 kg pulse flour, ferment for 5 days) diluted in 100 L water monthly to promote growth.",
        "Guidance": "Monitor weekly for pests."
    },
    {
        "index": 4,
        "disease_name": "Blueberry___healthy",
        "description": "Healthy blueberry plants have lush green foliage and firm, juicy berries. They thrive in acidic soils (pH 4.5–5.5).",
        "Possible Steps": "Maintain soil pH between 4.5 and 5.5.",
        "Organic_Solution": "Apply 10 kg neem cake mixed with 20 kg cow dung compost per hectare to maintain soil acidity and fertility. Spray 3 L Panchagavya diluted in 100 L water monthly to enhance plant vigor.",
        "Guidance": "Ensure proper drainage."
    },
    {
        "index": 5,
        "disease_name": "Cherry___Powdery_mildew",
        "description": "Powdery mildew, caused by *Podosphaera clandestina*, forms white, powdery spots on leaves and shoots, reducing photosynthesis. It thrives in warm, dry conditions but can spread in Tamil Nadu’s humid climate.",
        "Possible Steps": "Improve air circulation by pruning.",
        "Organic_Solution": "Mix 1 L buttermilk with 9 L water and spray weekly to suppress fungal growth. Add 50 ml neem oil to enhance efficacy. Apply 10 kg wood ash per hectare to soil to reduce fungal spores.",
        "Guidance": "Avoid overhead watering."
    },
    {
        "index": 6,
        "disease_name": "Cherry___healthy",
        "description": "Healthy cherry plants display glossy green leaves and robust fruit production. Regular care ensures disease resistance.",
        "Possible Steps": "Regular pruning and fertilization.",
        "Organic_Solution": "Spray 5 L neem oil diluted in 100 L water monthly. Apply 500 kg cow dung compost per hectare every 3 months to maintain soil health.",
        "Guidance": "Monitor for pests and diseases weekly."
    },
    {
        "index": 7,
        "disease_name": "Corn___Cercospora_leaf_spot",
        "description": "Cercospora leaf spot, caused by *Cercospora zeae-maydis*, creates grayish-white spots with dark borders on corn leaves, reducing yield. It thrives in warm, humid conditions.",
        "Possible Steps": "Rotate crops annually.",
        "Organic_Solution": "Prepare compost tea by steeping 10 kg well-decomposed cow dung in 50 L water for 5 days, strain, and spray weekly. Mix with 3 L Panchagavya for added benefits. Apply 10 kg neem cake per hectare to soil.",
        "Guidance": "Avoid planting corn in the same field consecutively."
    },
    {
        "index": 8,
        "disease_name": "Corn___Common_rust",
        "description": "Common rust, caused by *Puccinia sorghi*, produces orange pustules on corn leaves, impacting photosynthesis. It favors cool, moist conditions.",
        "Possible Steps": "Plant resistant varieties.",
        "Organic_Solution": "Mix 5 kg wood ash with 100 L water and spray biweekly. Combine with 3 L Amrit Jal (10 kg cow dung, 5 L cow urine, 1 kg jaggery, fermented 3 days) per hectare as a foliar spray.",
        "Guidance": "Ensure proper spacing for air circulation."
    },
    {
        "index": 9,
        "disease_name": "Corn___Northern_leaf_blight",
        "description": "Northern leaf blight, caused by *Exserohilum turcicum*, forms long, grayish lesions on corn leaves, reducing yield. It thrives in wet, warm weather.",
        "Possible Steps": "Remove crop debris after harvest.",
        "Organic_Solution": "Mix 50 g baking soda with 10 L water and 50 ml neem oil, spray weekly. Apply 20 kg fermented cow dung per hectare to enhance soil microbial activity.",
        "Guidance": "Rotate crops to reduce disease pressure."
    },
    {
        "index": 10,
        "disease_name": "Corn___healthy",
        "description": "Healthy corn plants have dark green leaves and strong stalks. Proper care prevents disease onset.",
        "Possible Steps": "Maintain proper irrigation.",
        "Organic_Solution": "Apply 500 kg cow dung compost per hectare every 3 months. Spray 3 L Jeevamrutham diluted in 100 L water monthly to boost growth.",
        "Guidance": "Monitor for pests and nutrient deficiencies."
    },
    {
        "index": 11,
        "disease_name": "Grape___Black_rot",
        "description": "Black rot, caused by *Guignardia bidwellii*, causes brown lesions on grape leaves and fruit, leading to mummified berries. It thrives in warm, humid conditions.",
        "Possible Steps": "Prune to improve air circulation.",
        "Organic_Solution": "Mix 5 kg wood ash with 100 L water and spray biweekly. Apply 3 L Panchagavya diluted in 100 L water weekly to boost plant immunity.",
        "Guidance": "Remove mummified fruit to reduce spores."
    },
    {
        "index": 12,
        "disease_name": "Grape___Esca",
        "description": "Esca, a fungal disease, causes leaf discoloration, tiger-stripe patterns, and wood decay in grapes. It affects vines in warm climates.",
        "Possible Steps": "Avoid overwatering.",
        "Organic_Solution": "Apply Trichoderma-based biofungicide (5 kg per hectare) to soil. Spray 3 L Amrit Jal diluted in 100 L water biweekly to enhance plant vigor.",
        "Guidance": "Prune infected wood and burn it."
    },
    {
        "index": 13,
        "disease_name": "Grape___Leaf_blight",
        "description": "Leaf blight, caused by *Pseudocercospora vitis*, produces dark spots with yellow halos on grape leaves, reducing photosynthesis. It thrives in humid conditions.",
        "Possible Steps": "Improve vineyard sanitation.",
        "Organic_Solution": "Spray 5 L neem oil diluted in 100 L water weekly. Apply 20 kg fermented cow dung per hectare to soil to suppress pathogens.",
        "Guidance": "Avoid overhead irrigation."
    },
    {
        "index": 14,
        "disease_name": "Grape___healthy",
        "description": "Healthy grape plants have vibrant leaves and firm fruit clusters. Regular care prevents disease.",
        "Possible Steps": "Maintain balanced fertilization.",
        "Organic_Solution": "Apply 5 L neem oil diluted in 100 L water monthly. Use 500 kg cow dung compost per hectare every 3 months.",
        "Guidance": "Monitor for pests and diseases."
    },
    {
        "index": 15,
        "disease_name": "Orange___Haunglongbing",
        "description": "Huanglongbing (HLB), caused by *Candidatus Liberibacter*, leads to yellowing leaves, fruit drop, and bitter, misshapen oranges. It is spread by psyllids and is a severe issue in citrus.",
        "Possible Steps": "Remove infected trees.",
        "Organic_Solution": "Plant marigolds around trees to repel psyllids. Spray 5 L neem oil diluted in 100 L water weekly to control vectors. Apply 3 L Panchagavya diluted in 100 L water biweekly to boost tree health.",
        "Guidance": "Control psyllid vectors with organic sprays."
    },
    {
        "index": 16,
        "disease_name": "Peach___Bacterial_spot",
        "description": "Bacterial spot, caused by *Xanthomonas campestris*, forms small, water-soaked spots on peach leaves and fruit, turning dark and sunken. It thrives in warm, wet conditions.",
        "Possible Steps": "Use resistant varieties.",
        "Organic_Solution": "Mix 100 g garlic with 1 L water, strain, add 50 ml neem oil, and spray weekly. Apply 20 kg cow dung compost per hectare to enhance soil health.",
        "Guidance": "Avoid overhead watering."
    },
    {
        "index": 17,
        "disease_name": "Peach___healthy",
        "description": "Healthy peach plants have glossy leaves and firm fruit. Proper care prevents disease onset.",
        "Possible Steps": "Prune annually.",
        "Organic_Solution": "Apply 500 kg cow dung compost per hectare every 3 months. Spray 3 L Jeevamrutham diluted in 100 L water monthly.",
        "Guidance": "Monitor for pests and diseases."
    },
    {
        "index": 18,
        "disease_name": "Pepper,_bell___Bacterial_spot",
        "description": "Bacterial spot, caused by *Xanthomonas campestris*, causes dark, water-soaked spots on bell pepper leaves and fruit, leading to yield loss. It thrives in humid conditions.",
        "Possible Steps": "Rotate crops.",
        "Organic_Solution": "Mix 100 g garlic with 1 L water, strain, add 50 ml neem oil, and spray weekly. Apply 10 kg neem cake per hectare to soil.",
        "Guidance": "Avoid overhead irrigation."
    },
    {
        "index": 19,
        "disease_name": "Pepper,_bell___healthy",
        "description": "Healthy bell pepper plants have dark green leaves and firm fruit. Regular care ensures vigor.",
        "Possible Steps": "Maintain proper spacing.",
        "Organic_Solution": "Apply 5 L neem oil diluted in 100 L water monthly. Use 500 kg cow dung compost per hectare every 3 months.",
        "Guidance": "Monitor for pests and nutrient deficiencies."
    },
    {
        "index": 20,
        "disease_name": "Potato___Early_blight",
        "description": "Early blight, caused by *Alternaria solani*, produces concentric rings (target spots) on potato leaves, leading to defoliation. It thrives in warm, wet conditions.",
        "Possible Steps": "Rotate crops and remove debris.",
        "Organic_Solution": "Mix 50 g baking soda with 10 L water and 50 ml neem oil, spray weekly. Apply 3 L Panchagavya diluted in 100 L water biweekly to boost plant immunity.",
        "Guidance": "Ensure proper spacing for air circulation."
    },
    {
        "index": 21,
        "disease_name": "Potato___Late_blight",
        "description": "Late blight, caused by *Phytophthora infestans*, forms water-soaked, gray-green spots on potato leaves, turning dark. It spreads rapidly in cool, wet conditions.",
        "Possible Steps": "Use resistant varieties.",
        "Organic_Solution": "Mix 5 kg wood ash with 100 L water and spray biweekly. Apply 3 L Amrit Jal diluted in 100 L water weekly to enhance resistance.",
        "Guidance": "Avoid overhead watering."
    },
    {
        "index": 22,
        "disease_name": "Potato___healthy",
        "description": "Healthy potato plants have lush green foliage and strong tubers. Proper care prevents disease.",
        "Possible Steps": "Maintain proper irrigation.",
        "Organic_Solution": "Apply 500 kg cow dung compost per hectare every 3 months. Spray 3 L Jeevamrutham diluted in 100 L water monthly.",
        "Guidance": "Monitor for pests and diseases."
    },
    {
        "index": 23,
        "disease_name": "Raspberry___healthy",
        "description": "Healthy raspberry plants have vibrant canes and juicy berries. Regular care ensures productivity.",
        "Possible Steps": "Prune canes annually.",
        "Organic_Solution": "Apply 5 L neem oil diluted in 100 L water monthly. Use 500 kg cow dung compost per hectare every 3 months.",
        "Guidance": "Ensure good air circulation."
    },
    {
        "index": 24,
        "disease_name": "Soybean___healthy",
        "description": "Healthy soybean plants have dark green leaves and robust pods. Proper care prevents disease.",
        "Possible Steps": "Maintain soil fertility.",
        "Organic_Solution": "Apply 500 kg cow dung compost per hectare every 3 months. Spray 3 L Jeevamrutham diluted in 100 L water monthly.",
        "Guidance": "Monitor for pests and nutrient deficiencies."
    },
    {
        "index": 25,
        "disease_name": "Squash___Powdery_mildew",
        "description": "Powdery mildew, caused by *Erysiphe cichoracearum*, forms white, powdery spots on squash leaves, reducing yield. It thrives in warm, dry conditions but spreads in humidity.",
        "Possible Steps": "Improve air circulation.",
        "Organic_Solution": "Mix 1 L buttermilk with 9 L water and 50 ml neem oil, spray weekly. Apply 10 kg wood ash per hectare to soil to reduce fungal spores.",
        "Guidance": "Avoid overhead watering."
    },
    {
        "index": 26,
        "disease_name": "Strawberry___Leaf_scorch",
        "description": "Leaf scorch, caused by *Diplocarpon earlianum*, produces dark purple to black spots on strawberry leaves, leading to reduced photosynthesis. It thrives in warm, wet conditions.",
        "Possible Steps": "Improve irrigation practices.",
        "Organic_Solution": "Spray 5 L neem oil diluted in 100 L water weekly. Apply 3 L Panchagavya diluted in 100 L water biweekly to enhance plant health.",
        "Guidance": "Ensure proper spacing for air circulation."
    },
    {
        "index": 27,
        "disease_name": "Strawberry___healthy",
        "description": "Healthy strawberry plants have green leaves and firm, red fruit. Regular care ensures vigor.",
        "Possible Steps": "Maintain soil moisture.",
        "Organic_Solution": "Apply 5 L neem oil diluted in 100 L water monthly. Use 500 kg cow dung compost per hectare every 3 months.",
        "Guidance": "Monitor for pests and diseases."
    },
    {
        "index": 28,
        "disease_name": "Tomato___Bacterial_spot",
        "description": "Bacterial spot, caused by *Xanthomonas campestris*, forms dark, water-soaked spots on tomato leaves and fruit, turning black. It thrives in warm, wet conditions.",
        "Possible Steps": "Use resistant varieties.",
        "Organic_Solution": "Mix 100 g garlic with 1 L water, strain, add 50 ml neem oil, and spray weekly. Apply 10 kg neem cake per hectare to soil.",
        "Guidance": "Avoid overhead irrigation."
    },
    {
        "index": 29,
        "disease_name": "Tomato___Early_blight",
        "description": "Early blight, caused by *Alternaria solani*, produces concentric rings (target spots) on tomato leaves, leading to defoliation. It thrives in warm, wet conditions.",
        "Possible Steps": "Rotate crops.",
        "Organic_Solution": "Mix 50 g baking soda with 10 L water and 50 ml neem oil, spray weekly. Apply 3 L Panchagavya diluted in 100 L water biweekly.",
        "Guidance": "Ensure proper spacing."
    },
    {
        "index": 30,
        "disease_name": "Tomato___Late_blight",
        "description": "Late blight, caused by *Phytophthora infestans*, forms water-soaked, gray-green spots on tomato leaves, turning dark. It spreads rapidly in cool, wet conditions.",
        "Possible Steps": "Use resistant varieties.",
        "Organic_Solution": "Mix 5 kg wood ash with 100 L water and spray biweekly. Apply 3 L Amrit Jal diluted in 100 L water weekly.",
        "Guidance": "Avoid overhead watering."
    },
    {
        "index": 31,
        "disease_name": "Tomato___Leaf_Mold",
        "description": "Leaf mold, caused by *Fulvia fulva*, causes yellowing leaves with grayish mold on the underside. It thrives in high humidity and warm conditions.",
        "Possible Steps": "Improve ventilation.",
        "Organic_Solution": "Spray 5 L neem oil diluted in 100 L water weekly. Apply 3 L Panchagavya diluted in 100 L water biweekly to boost immunity.",
        "Guidance": "Avoid high humidity conditions."
    },
    {
        "index": 32,
        "disease_name": "Tomato___Septoria_leaf_spot",
        "description": "Septoria leaf spot, caused by *Septoria lycopersici*, forms small spots with gray centers and yellow halos on tomato leaves. It spreads in wet conditions.",
        "Possible Steps": "Remove infected leaves.",
        "Organic_Solution": "Mix 100 g garlic with 1 L water, strain, add 50 ml neem oil, and spray weekly. Apply 20 kg fermented cow dung per hectare.",
        "Guidance": "Ensure proper spacing."
    },
    {
        "index": 33,
        "disease_name": "Tomato___Spider_mites",
        "description": "Spider mites cause stippling and yellowing on tomato leaves, with fine webbing visible. They thrive in hot, dry conditions.",
        "Possible Steps": "Introduce predatory mites.",
        "Organic_Solution": "Spray 5 L neem oil diluted in 100 L water weekly. Apply 3 L Jeevamrutham diluted in 100 L water biweekly to enhance plant vigor.",
        "Guidance": "Maintain humidity to deter mites."
    },
    {
        "index": 34,
        "disease_name": "Tomato___Target_Spot",
        "description": "Target spot, caused by *Corynespora cassiicola*, produces circular spots with concentric rings on tomato leaves. It thrives in warm, humid conditions.",
        "Possible Steps": "Remove infected leaves.",
        "Organic_Solution": "Mix 5 kg wood ash with 100 L water and spray biweekly. Apply 3 L Panchagavya diluted in 100 L water weekly.",
        "Guidance": "Avoid overhead irrigation."
    },
    {
        "index": 35,
        "disease_name": "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
        "description": "Tomato yellow leaf curl virus, spread by whiteflies, causes curled, yellow leaves and stunted growth. It is a severe issue in warm climates.",
        "Possible Steps": "Control whiteflies.",
        "Organic_Solution": "Plant marigolds to repel whiteflies. Spray 5 L neem oil diluted in 100 L water weekly. Apply 3 L Panchagavya diluted in 100 L water biweekly.",
        "Guidance": "Apply neem oil to control vectors."
    },
    {
        "index": 36,
        "disease_name": "Tomato___Tomato_mosaic_virus",
        "description": "Tomato mosaic virus causes mottled, yellow-green leaves and stunted growth. It spreads via contact and infected tools.",
        "Possible Steps": "Sanitize tools.",
        "Organic_Solution": "Remove and destroy infected plants. Spray 3 L Jeevamrutham diluted in 100 L water biweekly to boost healthy plant growth.",
        "Guidance": "Avoid handling plants when wet."
    },
    {
        "index": 37,
        "disease_name": "Tomato___healthy",
        "description": "Healthy tomato plants have dark green leaves and firm fruit. Regular care prevents disease onset.",
        "Possible Steps": "Maintain proper care.",
        "Organic_Solution": "Apply 5 L neem oil diluted in 100 L water monthly. Use 500 kg cow dung compost per hectare every 3 months.",
        "Guidance": "Monitor for pests and diseases."
    },
    {
        "index": 38,
        "disease_name": "Background_without_leaves",
        "description": "No plant leaves detected in the image, indicating an invalid input for diagnosis.",
        "Possible Steps": "Upload an image with leaves.",
        "Organic_Solution": "N/A",
        "Guidance": "Ensure the image focuses on plant leaves."
    }
]

with app.app_context():
    db.create_all()
    for entry in csv_data:
        existing_disease = Disease.query.filter_by(disease_name=entry['disease_name']).first()
        if existing_disease:
            # Update existing record
            existing_disease.description = entry['description']
            existing_disease.organic_solution = entry['Organic_Solution']
            existing_disease.guidance = entry['Guidance']
            existing_disease.possible_steps = entry['Possible Steps']
        else:
            # Insert new record
            disease = Disease(
                id=entry['index'] + 1,  # Match CSV index to DB ID (1-based)
                disease_name=entry['disease_name'],
                description=entry['description'],
                organic_solution=entry['Organic_Solution'],
                guidance=entry['Guidance'],
                possible_steps=entry['Possible Steps']
            )
            db.session.add(disease)
    db.session.commit()
    print("Disease table updated successfully.")
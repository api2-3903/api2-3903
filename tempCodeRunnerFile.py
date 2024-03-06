import replicate
import urllib.parse


# Now you can use `image_path` in your code to access the image file

#user data (will come from profile page later)
User_gender = "girl" # girl, boy, man, woman
# User_age = "20"
# User_height = "170" //not dealing in absolutes as it doesn't make sense in image generation
# User_weight = "50"
User_body_type = "slim" #slim, normal, fat
User_age = "teen" # old, young, adult, kid, baby 
User_height = "tall" # short, medium, tall
User_weight = "plus size" # underweight, normal, plus size 

#these attributes come from profile database under advance section only and will be picked up by AI 
# User_skin = "white" # white, black, asian, hispanic,
# User_eyes = "brown eyes" # brown eyes, blue eyes, green eyes, hazel eyes, black eyes
# User_ethnicity = "white" # white, black, asian, hispanic,
# User_glasses = " " # glasses , " "
# User_facial_hair = " " # beard , moustace, goatee , " "
# User_hair_length = "shoulder length hair" # shoulder length hair,  short hair , long hair
# User_hair_color = "black hair" # Ginger hair, brown hair, blonde hair, blue hair
# User_hair_style = "straight hair" #curly hair, wavy hair

#these attributes come from clothes database 
User_top_style = "casual" # formal, casual 
User_bottom_style = "casual" # formal, casual
User_top_color = "black" # black, white, red, blue,
User_bottom_color = "black" # black, white, red, blue,

#dynamic prompt template
prompt_template = f"# {User_age} {User_height} {User_weight} {User_body_type} {User_gender}  wearing"
if User_top_style:
    prompt_template += f" {User_top_style}"
if User_top_color:
    prompt_template += f" {User_top_color}"
prompt_template += " top with "
if User_bottom_style:
    prompt_template += f" {User_bottom_style}"
if User_bottom_color:
    prompt_template += f" {User_bottom_color}"
prompt_template += " bottom"

print(prompt_template)

# # Paths to image files ( drive)
# top_image_path = "https://drive.google.com/file/d/1PDy3xenOKmforYiuTgzGHulxl8qYtkcx/view?usp=drive_link"
# bottom_image_path = "https://drive.google.com/file/d/1-q9E6-LZUw1YXEHa8d5Svf44NMtmI-4h/view?usp=sharing"

top_image_path = "https://imgur.com/u5qraQp"
bottom_image_path = "https://imgur.com/pbNo5me"


# top_image_path = 'C:\\Users\Pratham Jain\SisterDear\WardrobeApp\tops\tshirt_black_plain.jpg'  # Absolute path
# bottom_image_path = 'C:/Users/Pratham Jain/SisterDear/WardrobeApp/bottoms/grey_jeans.png'  # Absolute path
# face_image_path = "C:\Users\Pratham Jain\SisterDear\WardrobeApp\faces\Kriti.jpg"


# # Encoding file paths into URI format
# top_image_uri = 'file:///' + urllib.parse.quote(top_image_path)
# bottom_image_uri = 'file:///' + urllib.parse.quote(bottom_image_path)



# output = replicate.run(
#     "konieshadow/fooocus-api-realistic:8958d6f677f825b57175bf644471fddfee6210a165cc20037323575a84d16afb",
#     input={
#         "prompt": prompt_template,
#         "cn_type1": "ImagePrompt",
#         "cn_type2": "ImagePrompt",
#         "cn_type3": "ImagePrompt",
#         "cn_type4": "ImagePrompt",
#         "sharpness": 2,
#         "image_seed": -1,
#         "uov_method": "Disabled",
#         "image_number": 1,
#         "guidance_scale": 3,
#         "refiner_switch": 0.5,
#         "negative_prompt": "unrealistic, saturated, high contrast, big nose, painting, drawing, sketch, cartoon, anime, manga, render, CG, 3d, watermark, signature, label",
#         "style_selections": "Fooocus V2,Fooocus Photograph,Fooocus Negative",
#         "uov_upscale_value": 0,
#         "outpaint_selections": "",
#         "outpaint_distance_top": 0,
#         "performance_selection": "Speed",
#         "outpaint_distance_left": 0,
#         "aspect_ratios_selection": "1152*896",
#         "outpaint_distance_right": 0,
#         "outpaint_distance_bottom": 0,
#         "inpaint_additional_prompt": ""
#     }
# )
# print(output)

output_image_temp = replicate.run(
            "konieshadow/fooocus-api-realistic:8958d6f677f825b57175bf644471fddfee6210a165cc20037323575a84d16afb",
            input={
                    "prompt": prompt_template,
                    "cn_img1": top_image_path,
                    "cn_stop1": 0.81,
                    "cn_weight1" : 0.8,
                    "cn_type1": "ImagePrompt",
                    "cn_img2": bottom_image_path,
                    "cn_stop2": 0.81,
                    "cn_weight2": 0.8,
                    "cn_type2": "ImagePrompt",
                    "cn_type3": "ImagePrompt",
                    "cn_type4": "ImagePrompt",
                    "sharpness": 2,
                    "image_seed": -1,
                    "uov_method": "Disabled",
                    "image_number": 1,
                    "guidance_scale": 3,
                    "refiner_switch": 0.5,
                    "negative_prompt": "unrealistic,mutilated pupils,saturated, high contrast, big nose, painting, drawing, sketch, cartoon, anime, manga, render, CG, 3d, watermark, signature, label",
                    "style_selections": "Fooocus V2,Fooocus Photograph,Fooocus Negative",
                    "uov_upscale_value": 0,
                    "outpaint_selections": "",
                    "outpaint_distance_top": 0,
                    "performance_selection": "Speed",
                    "outpaint_distance_left": 0,
                    "aspect_ratios_selection": "832*1216",
                    "outpaint_distance_right": 0,
                    "outpaint_distance_bottom": 0,
                    "inpaint_additional_prompt": ""
                }
            )

print(output_image_temp)

# output_image = replicate.run(
#             "konieshadow/fooocus-api-realistic:8958d6f677f825b57175bf644471fddfee6210a165cc20037323575a84d16afb",
#             input={
#                     "prompt": prompt_template,
#                     "cn_img1": top_image_uri,
#                     "cn_stop1": 0.25,
#                     "cn_weight1" : 0.3,
#                     "cn_type1": "ImagePrompt",

#                     "cn_img2": bottom_image_uri,
#                     "cn_stop2": 0.25,
#                     "cn_weight2": 0.3,
#                     "cn_type2": "ImagePrompt",

#                     "cn_img3": face_path_uri,
#                     "cn_stop3": 0.85,
#                     "cn_weight3" : 1.1,
#                     "cn_type3": "FaceSwap",

#                     "cn_img4": output_image_temp,
#                     "cn_stop4": 0.8,
#                     "cn_weight4" : 0.8,
#                     "cn_type4": "ImagePrompt",

#                     "sharpness": 2,
#                     "image_seed": -1,
#                     "uov_method": "Disabled",
#                     "image_number": 1,
#                     "guidance_scale": 3,
#                     "refiner_switch": 0.5,
#                     "negative_prompt": "unrealistic,mutilated pupils,saturated, high contrast, big nose, painting, drawing, sketch, cartoon, anime, manga, render, CG, 3d, watermark, signature, label",
#                     "style_selections": "Fooocus V2,Fooocus Photograph,Fooocus Negative",
#                     "uov_upscale_value": 0,
#                     "outpaint_selections": "",
#                     "outpaint_distance_top": 0,
#                     "performance_selection": "Speed",
#                     "outpaint_distance_left": 0,
#                     "aspect_ratios_selection": "768*1344",
#                     "outpaint_distance_right": 0,
#                     "outpaint_distance_bottom": 0,
#                     "inpaint_additional_prompt": ""
#                 }
#             )

#             # Display the rendered outfit image
# print(output_image)






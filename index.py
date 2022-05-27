from IPython.display import display 
from PIL import Image
import random
import json
import os

os.system('cls' if os.name=='nt' else 'clear')

def create_new_image(all_images, config):
    new_image = {}
    for layer in config["layers"]:
      new_image[layer["name"]] =  random.choices(layer["values"], layer["weights"])[0]
          
    for incomp in config["incompatibilities"]:
      for attr in new_image:
        if new_image[incomp["layer"]] == incomp["value"] and new_image[attr] in incomp["incompatible_with"]:
          return create_new_image(all_images, config)

    if new_image in all_images:
      return create_new_image(all_images, config)
    else:
      return new_image

def generate_unique_images(amount, config):
  print("Generating {} unique NFTs...".format(amount))
  pad_amount = len(str(amount));
  trait_files = {
  }
  for trait in config["layers"]:
    trait_files[trait["name"]] = {}
    for x, key in enumerate(trait["values"]):
      trait_files[trait["name"]][key] = trait["filename"][x];
  
  all_images = []
  for i in range(amount): 
    new_trait_image = create_new_image(all_images, config)

    if new_trait_image['Eyes'] in list(map(lambda x: x+ " Eyes", ["Ahegao", "Crying", "High", "Mangekyou Sharingan", "Rinne Sharingan", "Rinnegan", "Sharingan", "Love"])):
      new_trait_image['Glasses'] = 'None Glasses'
    
    if new_trait_image['Skin'] == "Robot Skin":
      new_trait_image['Top'] = 'None Top'

    if new_trait_image['Accessory'] == "None Accessory":
      new_trait_image['Hand'] = 'None Hand'
    else:
      skin_color = new_trait_image['Skin'][:-5]
      new_trait_image['Hand']= f'{skin_color} Hand'

    all_images.append(new_trait_image)

  i = 1
  for item in all_images:
      item["id"] = i
      i += 1

  for i, token in enumerate(all_images):
    attributes = []
    for key in token:
      if key != "id":
        layerData = [item for item in data["layers"] if item["name"] == key][0]
        valueI = layerData["values"].index(token[key])
        freq = layerData["weights"][valueI] / layerData["total"]

        if "None" not in token[key]:
          attributes.append({"trait_type": key, "value": token[key], "frequency": freq})
    token_metadata = {
        "id": token["id"],
        "name":  config["name"] + str(token["id"]),
        "attributes": attributes
    }
    with open('./metadata/' + str(token["id"]) + '.json', 'w') as outfile:
        json.dump(token_metadata, outfile, indent=4)

  with open('./metadata/all-objects.json', 'w') as outfile:
    json.dump(all_images, outfile, indent=4)
  
  for item in all_images:
    layers = []
    for index, attr in enumerate(item):
      if attr != 'id':
        layers.append([])
        layers[index] = Image.open(f'{config["layers"][index]["trait_path"]}/{trait_files[attr][item[attr]]}.png').convert('RGBA')

    if len(layers) == 1:
      rgb_im = layers[0].convert('RGB')
      file_name = str(item["id"]) + ".png"
      rgb_im.save("./images/" + file_name)
    elif len(layers) == 2:
      main_composite = Image.alpha_composite(layers[0], layers[1])
      rgb_im = main_composite.convert('RGB')
      file_name = str(item["id"]) + ".png"
      rgb_im.save("./images/" + file_name)
    elif len(layers) >= 3:
      main_composite = Image.alpha_composite(layers[0], layers[1])
      layers.pop(0)
      layers.pop(0)
      for index, remaining in enumerate(layers):
        main_composite = Image.alpha_composite(main_composite, remaining)
      rgb_im = main_composite.convert('RGB')
      file_name = str(item["id"]) + ".png"
      rgb_im.save("./images/" + file_name)
  
  # v1.0.2 addition
  print("\nUnique NFT's generated. After uploading images to IPFS, please paste the CID below.\nYou may hit ENTER or CTRL+C to quit.")
  cid = input("IPFS Image CID (): ")
  if len(cid) > 0:
    if not cid.startswith("ipfs://"):
      cid = "ipfs://{}".format(cid)
    if cid.endswith("/"):
      cid = cid[:-1]
    for i, item in enumerate(all_images):
      with open('./metadata/' + str(item["id"]) + '.json', 'r') as infile:
        original_json = json.loads(infile.read())
        original_json["image"] = original_json["image"].replace(config["baseURI"]+"/", cid+"/")
        with open('./metadata/' + str(item["id"]) + '.json', 'w') as outfile:
          json.dump(original_json, outfile, indent=4)


backgrounds = list(map(lambda x: x + " Background", ["Apricot", "Tie-Dye", "Blueberry", "Flames", "Hot Pink", "Lilac", "Money", "Raspberry", "Striped", "Strawberry", "Trippy", "Space"]))
backgrounds_weights = [14,4,14,3,14,14,3,14,4,14,2,2]
backgrounds_total = sum(backgrounds_weights)
backgrounds_data = {
  "name": "Background",
  "trait_path": "trait-layers/Backgrounds",
  "filename": backgrounds,
  "values": backgrounds,
  "weights": backgrounds_weights,
  "total": backgrounds_total
}

lips = list(map(lambda x: x + " Lips", ["Ahegao", "Basic", "Berry", "Deep Purple", "Fangs", "Fusia", "Glossy Grape", "Bite", "Matte Pink", "Orange", "Peach", "Red", "Tongue"]))
lips_weights = [1,52,5,5,1,5,5,5,5,5,5,5,1]
lips_total = sum(lips_weights)
lips_data = {
  "name": "Lips",
  "trait_path": "trait-layers/Lips",
  "filename": lips,
  "values": lips,
  "weights": lips_weights,
  "total": lips_total
}

tops = list(map(lambda x: x + " Top", ["Alliance", "Basic", "Mavericks", "Shell", "Bikini", "Celtics", "Harness", "Heart", "Heat", "HODL", "Horde", "Keikogi", "Monogram", "Pay Me", "Scout", "Sparkly", "Tourist", "Warriors", "Cheetah", "Denim"]))
tops_weights = [2,27,3,5,5,3,5,5,3,5,2,1,5,5,1,5,5,3,5,5]
tops_total = sum(tops_weights)
tops_data = {
  "name": "Top",
  "trait_path": "trait-layers/Tops",
  "filename": tops + ["None Top"],
  "values": tops + ["None Top"],
  "weights": tops_weights + [0],
  "total": tops_total
}

necklaces = list(map(lambda x: x + " Necklace", ["AVAX", "Baddie", "Cat", "Emerald", "Heart", "Infinity Stones", "Hokage", "Pearl", "Ribbon", "PokeBall", "Punk", "Xiku", "Millennium Puzzle", "None"]))
necklaces_weights = list(map(lambda x: x * 10, [3,3,6,6,6,2,3,6,6,0.5,6,2,0.5,50]))
necklaces_total = sum(necklaces_weights)
necklaces_data = {
  "name": "Necklace",
  "trait_path": "trait-layers/Necklaces",
  "filename": necklaces,
  "values": necklaces,
  "weights": necklaces_weights,
  "total": necklaces_total
}

accessories = list(map(lambda x: x + " Accessory", ["AVAX Bag", "Basketball Bag", "Bucket Bag", "Crocodile Bag", "Dragonball", "Ezreal Glove", "Heart Bag", "Infinity Gauntlet", "Kitty Bag", "Lips Bag", "Masterball", "Monogram Bag", "Pokeball", "Puppy Bag", "Star Bag", "None"]))
accessories_weights = [5, 1, 5, 5,2,2,4,2,3,5,1,5,2,3,5,50]
accessories_total = sum(accessories_weights)
accessories_data = {
  "name": "Accessory",
  "trait_path": "trait-layers/Accessories",
  "filename": accessories,
  "values": accessories,
  "weights": accessories_weights,
  "total": accessories_total
}

eyes = list(map(lambda x: x+ " Eyes", ["Ahegao", "Basic", "Brown", "Crying", "Deep Blue", "Dust Pink", "Dust Red", "Fusia", "Grey", "High", "Light Blue", "Love", "Mangekyou Sharingan", "Olive", "Orange", "Purple", "Rinnegan", "Rinne Sharingan", "Rusty Red", "Sharingan", "Yellow"]))
eyes_weights = [4,15,5,4,5,5,5,5,5,4,5,2,3,5,5,5,3,2,5,3,5]
eyes_total = sum(eyes_weights)
eyes_data = {
  "name": "Eyes",
  "trait_path": "trait-layers/Eyes",
  "filename": eyes,
  "values": eyes,
  "weights": eyes_weights,
  "total": eyes_total
}

glasses = list(map(lambda x: x+ " Glasses", ["60s", "Batgirl", "Firefly", "Big Round", "Scanner", "Kurt", "Sci-Fi", "None", "50s", "2000s"]))
glasses_weights = [6,4,4,6,3,4,3,68,6,6]
glasses_total = sum(glasses_weights)
glasses_data = {
  "name": "Glasses",
  "trait_path": "trait-layers/Glasses",
  "filename": glasses,
  "values": glasses,
  "weights": glasses_weights,
  "total": glasses_total
}

hair = list(map(lambda x: x+ " Hair", ["Balled Pigtails", "Basic", "Blonde Afro", "Blonde Ponytail", "Blue Afro Puffs", "Bow Updo", "Brown Pigtails", "Brunette", "Curly Red", "Fluffy Pink", "Ginger", "Grape Bun", "Lilac Wavy", "Messy Buns", "Pink Buns", "Pink Ponytail", "Purple Pigtails", "Rainbow Pigtails", "Silver"]))
hair_weights = [4,10,4,6,5,6,6,6,3,4,6,6,4,6,5,6,5,3,5]
hair_total = sum(hair_weights)
hair_data = {
  "name": "Hair",
  "trait_path": "trait-layers/Hair",
  "filename": hair,
  "values": hair,
  "weights": hair_weights,
  "total": hair_total
}

makeup = list(map(lambda x:x+" Makeup", ["None", "Blush", "Freckles", "Heart Stickers", "Bowie", "Wet Mascara", "Smokey Eye", "Stars Stickers"]))
makeup_weights = [70,10,10,3,1,1,2,3]
makeup_total = sum(makeup_weights)
makeup_data = {
  "name": "Makeup",
  "trait_path": "trait-layers/Makeup",
  "filename": makeup,
  "values": makeup,
  "weights": makeup_weights,
  "total": makeup_total
}

ma = list(map(lambda x:x+" Mouth Accessory", ["None", "Blunt", "Cig", "Rose", "Gum"]))
ma_weights = [84,3,3,5,5]
ma_total = sum(ma_weights)
ma_data = {
  "name": "Mouth Accessory",
  "trait_path": "trait-layers/Mouth Accessories",
  "filename": ma,
  "values": ma,
  "weights": ma_weights,
  "total": ma_total
}

ha = list(map(lambda x:x+" Hair Accessory", ["None", "Baddies Clip", "Black Cat", "Bunny", "Butterflies", "Halo", "Headset", "Lips Clip", "Monogram Bow", "Shinobi Headband", "Rose", "Star Pin", "Tiara", "White Cat"]))
ha_weights = [50,5,4,4,3,2,3,5,5,3,5,5,2,4]
ha_total = sum(ha_weights)
ha_data = {
  "name": "Hair Accessory",
  "trait_path": "trait-layers/Hair Accessories",
  "filename": ha,
  "values": ha,
  "weights": ha_weights,
  "total": ha_total
}

skin_colors = ["Alien", "Beige", "Deep Brown", "Pale", "Robot", "Tan"]

skin = list(map(lambda x: x + " Skin", skin_colors))
skin_weights = [6,24,24,24,4,24]
skin_total = sum(skin_weights)
skin_data = {
  "name": "Skin",
  "trait_path": "trait-layers/Skin",
  "filename": skin,
  "values": skin,
  "weights": skin_weights,
  "total": skin_total
}

hand = list(map(lambda x: x + " Hand", skin_colors))
hand_data = {
  "name": "Hand",
  "trait_path": "trait-layers/Hands",
  "filename": hand + ["None Hand"],
  "values": hand + ["None Hand"],
  "weights": skin_weights + [0],
  "total": skin_total
}

ha_inc_names = list(map(lambda x: x+ " Hair Accessory", ["Bunny", "Shinobi Headband", "Headset"])) 
hair_inc_names = list(map(lambda x: x+ " Hair", ["Ginger", "Bow Updo", "Fluffy Pink"]))
ha_inc = []
for x in ha_inc_names:
  for y in hair_inc_names:
    ha_inc.append({
      "layer": "Hair Accessory",
      "value": x,
      "incompatible_with": y
    })

hair_inc_names = list(map(lambda x: x + " Hair", ["Blue Afro Puffs", "Blonde Afro"]))
skin_inc_names = list(map(lambda x: x + " Skin", ["Beige", "Pale"]))
hair_inc = []
for x in hair_inc_names:
  for y in skin_inc_names:
    ha_inc.append({
      "layer": "Hair",
      "value": x,
      "incompatible_with": y
    })

necklace_inc = []
for x in necklaces_data["values"]:
  necklace_inc.append({
    "layer": "Necklace",
    "value": x,
    "incompatible_with": "Scout Top"
  })

# eye_inc_names = list(map(lambda x: x+ " Eyes", ["Ahegao", "Crying", "High", "Mangekyou Sharingan", "Rinne Sharingan", "Rinnegan", "Sharingan", "Love"]))
# eye_inc = []
# for x in glasses_data["values"]:
#   for y in eye_inc_names:
#     eye_inc.append({
#       "layer": "Glasses",
#       "value": x,
#       "incompatible_with": y
#     })

data = {
  "layers": [
    backgrounds_data,
    skin_data,
    makeup_data,
    hair_data,
    tops_data,
    necklaces_data,
    eyes_data,
    lips_data,
    ma_data,
    hand_data,
    ha_data,
    glasses_data,
    accessories_data,
  ],
  "incompatibilities": ha_inc + hair_inc + necklace_inc,
  "name": "Bounty Baddies ",
}

generate_unique_images(1000, data)
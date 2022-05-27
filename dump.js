import Axios from "axios"
import { createRequire } from "module"; // Bring in the ability to create the 'require' method
const require = createRequire(import.meta.url); // construct the require method

const DUMP_API = 'https://n8l1kfybxj.execute-api.us-east-1.amazonaws.com/';

const newStat = (r, cat, n, w) => ({
    names: n.map(x => `${x} ${cat}`),
    weights: w,
    rarity: r
})

const rarities = {
    Legendary: 60,
    Epic: 30,
    Rare: 6,
    Uncommon: 3,
    Common: 1,
}

const stats = {
    'Background': newStat({2: "Legendary", 3: "Epic", 4: "Rare", 14: "Common"}, "Background", ["Apricot", "Tie-Dye", "Blueberry", "Flames", "Hot Pink", "Lilac", "Money", "Raspberry", "Striped", "Strawberry", "Trippy", "Space"],[14,4,14,3,14,14,3,14,4,14,2,2]),
    'Lips': newStat({1: "Legendary", 5: "Rare"}, "Lips", ["Ahegao", "Basic", "Berry", "Deep Purple", "Fangs", "Fusia", "Glossy Grape", "Bite", "Matte Pink", "Orange", "Peach", "Red", "Tongue"],[1,52,5,5,1,5,5,5,5,5,5,5,1]),
    'Top': newStat({1: "Legendary", 2: "Epic", 3: "Rare", 5: "Uncommon", 27: "Common"}, "Top",["Alliance", "Basic", "Mavericks", "Shell", "Bikini", "Celtics", "Harness", "Heart", "Heat", "HODL", "Horde", "Keikogi", "Monogram", "Pay Me", "Scout", "Sparkly", "Tourist", "Warriors", "Cheetah", "Denim"],[2,27,3,5,5,3,5,5,3,5,2,1,5,5,1,5,5,3,5,5]),
    'Necklace': newStat({"0.5": "Legendary", 2: "Epic", 3: "Rare", 6: "Uncommon"}, "Necklace", ["AVAX", "Baddie", "Cat", "Emerald", "Heart", "Infinity Stones", "Hokage", "Pearl", "Ribbon", "PokeBall", "Punk", "Xiku", "Millennium Puzzle", "None"],[3,3,6,6,6,2,3,6,6,0.5,6,2,0.5,50]),
    'Accessory': newStat({1: "Legendary", 2: "Epic", 3: "Rare", 4: "Uncommon", 5: "Uncommon" }, "Accessory", ["AVAX Bag", "Basketball Bag", "Bucket Bag", "Crocodile Bag", "Dragonball", "Ezreal Glove", "Heart Bag", "Infinity Gauntlet", "Kitty Bag", "Lips Bag", "Masterball", "Monogram Bag", "Pokeball", "Puppy Bag", "Star Bag", "None"],[5, 1, 5, 5,2,2,4,2,3,5,1,5,2,3,5,50]),
    "Eyes": newStat({2: "Legendary", 3: "Epic", 4: "Rare", 5: "Uncommon", 15: "Basic"}, "Eyes", ["Ahegao", "Basic", "Brown", "Crying", "Deep Blue", "Dust Pink", "Dust Red", "Fusia", "Grey", "High", "Light Blue", "Love", "Mangekyou Sharingan", "Olive", "Orange", "Purple", "Rinnegan", "Rinne Sharingan", "Rusty Red", "Sharingan", "Yellow"],[4,15,5,4,5,5,5,5,5,4,5,2,3,5,5,5,3,2,5,3,5]),
    "Glasses": newStat({3: "Legendary", 4: "Epic", 6: "Rare"}, "Glasses", ["60s", "Batgirl", "Firefly", "Big Round", "Scanner", "Kurt", "Sci-Fi", "None", "50s", "2000s"],[6,4,4,6,3,4,3,68,6,6]),
    "Hair": newStat({3: "Legendary", 4: "Epic", 5: "Rare", 6: "Uncommon", 10: "Common"}, "Hair",["Balled Pigtails", "Basic", "Blonde Afro", "Blonde Ponytail", "Blue Afro Puffs", "Bow Updo", "Brown Pigtails", "Brunette", "Curly Red", "Fluffy Pink", "Ginger", "Grape Bun", "Lilac Wavy", "Messy Buns", "Pink Buns", "Pink Ponytail", "Purple Pigtails", "Rainbow Pigtails", "Silver"],[4,10,4,6,5,6,6,6,3,4,6,6,4,6,5,6,5,3,5]),
    "Makeup": newStat({1: "Legendary", 2: "Epic", 3: "Rare", 10: "Uncommon", 70: "Common"}, "Makeup", ["None", "Blush", "Freckles", "Heart Stickers", "Bowie", "Wet Mascara", "Smokey Eye", "Stars Stickers"], [70,10,10,3,1,1,2,3]),
    "Mouth Accessory": newStat({3: "Legendary", 5: "Epic", 84: "Common"}, "Mouth Accessory",["None", "Blunt", "Cig", "Rose", "Gum"], [84,3,3,5,5]),
    "Hair Accessory": newStat({2: "Legendary", 3: "Epic", 4: "Rare", 5: "Uncommon", 50: "Common"}, "Hair Accessory", ["None", "Baddies Clip", "Black Cat", "Bunny", "Butterflies", "Halo", "Headset", "Lips Clip", "Monogram Bow", "Shinobi Headband", "Rose", "Star Pin", "Tiara", "White Cat"], [50,5,4,4,3,2,3,5,5,3,5,5,2,4]),
    "Skin": newStat({4: "Legendary", 6: "Epic", 24: "Common"}, "Skin", ["Alien", "Beige", "Deep Brown", "Pale", "Robot", "Tan"], [6,24,24,24,4,24]),
}

const makeUltra = (id, value) => ({
    id,
    name: `Bounty Baddies ${id}`,
    attributes: [
        { trait_type: "Ultra-Rare Baddies", frequency: "0.1%", value, rarity: "Ultra-Rare" }
    ],
    score: 1000
})

const dump = async() => {
    for (let i=1; i<1001; i++) {
        console.log(i)

        let data = require(`./metadata/${i}.json`)
        if (i === 12) {
            data = makeUltra(i, 'Android 18')
        } else if (i === 50) {
            data = makeUltra(i, 'Princess Leia')
        } else if (i === 101) {
            data = makeUltra(i, 'Harley Quinn')
        } else if (i === 158) {
            data = makeUltra(i , 'Scarlett Witch')
        } else if (i === 211) {
            data = makeUltra(i , 'Storm')
        } else if (i === 304) {
            data = makeUltra(i, 'Sarada')
        } else if (i === 420) {
            data = makeUltra(i, 'Misty')
        } else if (i === 641) {
            data = makeUltra(i, 'Mulan')
        } else if (i === 776) {
            data = makeUltra(i, 'Katara')
        } else if (i === 993) {
            data = makeUltra(i, 'Wonder Woman')
        } else {
            let score = 0
            const attr = data.attributes
                .filter(a => !a.value.includes("Basic") && !a.value.includes("None") && a["trait_type"] !== "Hand")
                .map(a => {
                    const cat = stats[a["trait_type"]]
                    const index = cat.names.indexOf(a.value)
                    const frequency = cat.weights[index].toString() + "%"
                    const rarity = cat.rarity[cat.weights[index]] || ""
                    score += rarities[rarity]
    
                    return {
                        ...a,
                        frequency,
                        rarity
                    }
                })
            data.attributes = attr
            data.score = score
        }

        await Axios.post(DUMP_API, data)
    }
}

dump()
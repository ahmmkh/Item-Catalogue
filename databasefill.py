from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, CategoryItem, Base

engine = create_engine('sqlite:///items.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Category 1
Soccer = Category(name='Soccer')
session.add(Soccer)
session.commit()

BasketBall = Category(name='BasketBall')
session.add(BasketBall)
session.commit()

BaseBall = Category(name='BaseBall')
session.add(BaseBall)
session.commit()

Frisbee = Category(name='Frisbee')
session.add(Frisbee)
session.commit()

SnowBoarding = Category(name='SnowBoarding')
session.add(SnowBoarding)
session.commit()

RockClimbing = Category(name='SnowBoarding')
session.add(RockClimbing)
session.commit()

Hiking = Category(name='SnowBoarding')
session.add(Hiking)
session.commit()

Hockey = Category(name='SnowBoarding')
session.add(Hockey)
session.commit()

#items for soccer
soccerShort = CategoryItem(name='Umbro Youth Knit Soccer Shorts', description='Gear your '
+'young athlete up for success with the Umbro Youth Knit Soccer Shorts. These '
+'lightweight, regular fit training shorts are equipped with moisture-wicking '
+'performance for cool, dry wear and excellent breathability. An elastic '
+'waistband is complete with an internal drawcord for a secure, adjustable fit.'
,price='$9.97',picture_url='img/soccer-shorts.png',category=Soccer)
session.add(soccerShort)
session.commit()

soccerBall = CategoryItem(name='Nike Barcelona Pitch Soccer Ball', description='Power '
+'through your next training session under the crest of Barca with the Nike '
+'Barcelona Pitch Soccer Ball. The Pitch features a durable TPU casing and '
+'machine-stitched panels, which help minimize potential abrasions and tears '
+'as you continue to develop various skills.',price='$25.00',
picture_url='img/soccer-ball.png',category=Soccer)
session.add(soccerBall)
session.commit()

soccerShoes = CategoryItem(name="adidas Men's Nemeziz Messi 17+ 360 Agility FG Soccer Cleats",
description='Just when you thought the technology could not get more advanced in your '
+'cleats the Nemeziz Messi 17+ 360 Agility re-writes the script. An Agility '
+'Knit 2.0 forefoot delivers a perfect fit and fantastic responsiveness from '
+'the first wear. Torsion Tape 360 Agility Bandage system is inspired by sports '
+'taping and offers you unmatched mobility, support and a revolutionary fit '
+'experience. The adidas Nemeziz Messi 17+ 360 Agility FG soccer cleat has a '
+'lightweight TORSIONFRAME outsole with TORSION RIBS that provide exceptional '
+'power, speed and push off support on natural grass pitches.'
,price='$289.99',picture_url='img/soccer-shoes.png',category=Soccer)
session.add(soccerShoes)
session.commit()

#items for BasketBall
BasketballBall = CategoryItem(name='Wilson Evolution Official Basketball (29.5")',
description='The preferred ball of many high school and college athletes, '
+'the Wilson Evolution Game Basketball is among the top performers in its '
+'class. Cushion Core Technology combines low-density sponge rubber and '
+'ultra-durable butyl rubber, producing a basketball with exceptional feel '
+'and unmatched durability. Constructed with a microfiber cover that is '
+'exclusively designed for the indoor court, the Wilson Official Evolution '
+'Game Basketball is a true champion.',price='$59.99',
picture_url='img/basketball-ball.png',category=BasketBall)
session.add(BasketballBall)
session.commit()

BasketballShirt = CategoryItem(name='Nike Mens Dry Showtime Full Zip Basketball '
+'Hoodie',description='Warm up comfortably to perform like a champion in the '
+'Nike Mens Dry Showtime Full Zip Basketball Hoodie. Its Nike Dry fabric '
+'wicks sweat for a cool, dry feel, while the HyperAlert hood allows for '
+'optimal peripheral vision and hearing. Shaped, elastic cuffs secure the fit, '
+'and side vents promote a full range of motion. Never crash under pressure '
+'again with the Dry Showtime Full Zip hoodie.',price='$90.00',
picture_url='img/basketball-shirt.png',category=BasketBall)
session.add(BasketballShirt)
session.commit()

BasketballShoes = CategoryItem(name='adidas Mens Dual Threat 2017 Basketball '
+'Shoes',description='Designed with a mid-cut silhouette, these sneakers blend '
+'support and stability, making them versatile enough for all positions on '
+'court. The updated cushioning system includes a secure foam collar to '
+'improve your fit at the ankle, and a foam midsole that provides lightweight '
+'cushioning on every landing. To round out these basketball sneakers, a '
+'circular traction outsole provides impressive grip perfect for fast cuts and '
+'quick directional changes. Rubber is used in the outsole to add durability, '
+'while synthetic overlays increase stability in key areas.',price='$44.98',
picture_url='img/basketball-shoes.png',category=BasketBall)
session.add(BasketballShoes)
session.commit()


#items for BaseBall
BaseballGloves = CategoryItem(name='Nokona 11.5 inches Classic Walnut Series Glove',
description='The Nokona 11.5 inches Classic Walnut Series Glove will deliver the '
+'durability and comfort you need to perform at an optimal level. Constructed '
+'of legendary Walnut Crunch leather, this American-made glove is soft and '
+'supple once broken in, but remains sturdy and strong season after season. '
+'The 11.5 inches Classic Walnut Baseball Glove features a Modified Trap web that is '
+'perfect for any infield position.',price='$239.99',
picture_url='img/baseball-gloves.png',category=BaseBall)
session.add(BaseballGloves)
session.commit()

BaseballHelmet = CategoryItem(name='Under Armour OSFM Solid Molded Batting Helmet',
description='The Under Armour OSFM Batting Helmet offers superior protection '
+'while maintaining maximum comfort. A high impact resistant ABS plastic shell '
+'with large vents throughout the helmet offers maximum breathability for '
+'comfort as the game heats up. Wrapped earpieces ensure greater durability '
+'and performance all season long. the UA Batting Helmet also features '
+'pre-mounted hardware for optional facemask attachment .',price='$27.97',
picture_url='img/baseball-helmet.png',category=BaseBall)
session.add(BaseballHelmet)
session.commit()

BaseballBats = CategoryItem(name='Easton S750 USA Youth Bat 2018',
description='Designed with a durable aluminum barrel, the 2018 Easton S750 '
+'USA Bat also includes an extended barrel design to enlarge the sweet spot.',
price='$99.99',picture_url='img/baseball-bats.png',category=BaseBall)
session.add(BaseballBats)
session.commit()


#items for Frisbee
FrisbeeDisk = CategoryItem(name='Innova Regular Mini Marker Disc',
description='Whether you are joining tournament play or just playing with '
+'friends, use the Innova Regular Mini Marker Disc to mark your lie and keep '
+'the course clean. Made from lightweight plastic, this 10 cm disc is perfect '
+'for keeping track of your place on the course without hindering the throws of'
+'other players. It is necessary for tournament play and a nice courtesy among '
+'friends as well. Keep your course player-friendly by using the Mini Marker Disc.',
price='$1.50',picture_url='img/frisbee-disk.png',category=Frisbee)
session.add(FrisbeeDisk)
session.commit()


#items for SnowBoarding
SnowBoardingGoggles = CategoryItem(name='Giro Adult Verge Zoom Snow Goggles',
description='Made for a better view, the Giro Adult Verge Zoom Snow Goggles '
+'deliver awesome features with great performance. You will love the Expansion '
+'View technology for a wider field of view, while the thermoformed lenses '
+'team up with anti-fog coating for a clear, optimal view. A mid-size frame '
+'with plush foam keeps you comfortable all season long.', price='$17.99',
picture_url='img/snowboarding-goggles.png',category=SnowBoarding)
session.add(SnowBoardingGoggles)
session.commit()

SnowBoardingBoards = CategoryItem(name='Burton Youth Riglet 2014-2015 Snowboard',
description='Designed specifically for budding snowboarders aged two through '
+'six, the Burton Youth Riglet Snowboard will deliver hours of snow day fun. '
+'The Flat Top ensures plenty of stability and balance, making it perfect for '
+'beginners. The grippy EVA foot pad helps little ones stay on the board, and '
+'the included Riglet Reel makes it easy to pull your little one around so they '
+'can get used to the feel of the board.', price='$99.95',
picture_url='img/snowboarding-boards.png',category=SnowBoarding)
session.add(SnowBoardingBoards)
session.commit()


#items for RockClimbing
RockClimbingCords = CategoryItem(name='Coghlans Sleeping Bag Bungee Cords',
description='For an easy and convenient way to tote your sleeping bag on your '
+'next camping or backpacking trip, try the Coghlans Sleeping Bag Bungee '
+'Cords. You can rest assured knowing your sleeping bag is secure using the '
+'two included 30 inches long cords.', price='$2.49',
picture_url='img/rockclimbing-cords.png',category=RockClimbing)
session.add(RockClimbingCords)
session.commit()

RockClimbingCords = CategoryItem(name='Nite Ize S-Biner Ahhh Carabiner and '
+'Bottle Opener',description='With the Nite Ize® S-Biner® Ahhh Carabiner and '
+'Bottle Opener you can be both practical and the life of the party at the '
+'same time! Both ends of the S-Biner® feature a carabiner with a gate '
+'closure, so you can clip one end and hang or store keys, water bottles, '
+'lanterns and more from the other end. Best of all, either side functions as '
+'a bottle opener, so you’re always prepared when you get thirsty.', price='$2.99',
picture_url='img/rockclimbing-opener.png',category=RockClimbing)
session.add(RockClimbingCords)
session.commit()


#items for Hiking
RockClimbingCords = CategoryItem(name='Coghlans Sleeping Bag Bungee Cords',
description='For an easy and convenient way to tote your sleeping bag on your '
+'next camping or backpacking trip, try the Coghlans Sleeping Bag Bungee '
+'Cords. You can rest assured knowing your sleeping bag is secure using the '
+'two included 30 inches long cords.', price='$2.49',
picture_url='img/rockclimbing-cords.png',category=Hiking)
session.add(RockClimbingCords)
session.commit()


print("added menu items!")

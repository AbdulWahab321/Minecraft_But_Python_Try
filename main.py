from ursina import * 
from ursina.prefabs.first_person_controller import FirstPersonController
import tkinter as tk

startRun = False

class HelpWin:
	def __init__(self):

		root = tk.Tk()

		tk.Label(text="""
Press 'Q' to Pause
 Press 'R' to resume
 		Press 'E' to enter Inventory 		
		""").pack()

		def startApp():
			global startRun
			root.destroy()
			startRun = True


		btn = tk.Button(text="Continue", bg="white", fg="black", command=lambda:startApp())
		btn.pack()
		root.mainloop()

HelpWin()
while True:
	if startRun:
		app = Ursina()
		grass_texture = load_texture('assets/grass_block2.png')
		stone_texture = load_texture('assets/stone_block2.png')
		brick_texture = load_texture('assets/brick1.png')
		dirt_texture  = load_texture('assets/dirt.png')
		sky_texture   = load_texture('assets/skybox.png')
		arm_texture   = load_texture('assets/arm_texture.png')
		punch_sound   = Audio('assets/punch_sound',loop = False, autoplay = False)


		block_pick = 1

		window.fps_counter.enabled = False
		window.exit_button.visible = True
		window.cursor_hidden = True
		window.fullscreen = True

		def setItem(item_variable,item_name,block_pick_number):
		   global block_pick
		   if item_variable == item_name:
			   block_pick = block_pick_number



		class Inventory():
			def __init__(self):
				from PIL import Image, ImageTk

				root = tk.Tk()
				lstbox = tk.Listbox(root)
				lstbox.insert(0,"Grass Block","Dirt","Stone","Brick")

				def setInventory():
					item = ""
					for i in lstbox.curselection():
						item = lstbox.get(i)

					setItem(item,"Grass Block",1)
					setItem(item , "Dirt", 4)
					setItem(item , "Stone", 2)
					setItem(item , "Brick", 3)

					root.destroy()
				btn = tk.Button(root,text="Select",bg = "white",fg="black",command=lambda:setInventory())
				lstbox.pack()
				btn.pack()
				root.mainloop()
		def update():
			global block_pick



			if held_keys['e']:Inventory()
			if held_keys['q']:player.disable()
			elif held_keys['r']:player.enable()
			if held_keys['left mouse'] or held_keys['right mouse']:
				hand.active()
			else:
				hand.notActive()

			if held_keys['1']: block_pick = 1
			if held_keys['2']: block_pick = 2
			if held_keys['3']: block_pick = 3
			if held_keys['4']: block_pick = 4

		class Voxel(Button):
			def __init__(self, position = (0,0,0), texture = grass_texture):
				return super().__init__(
					parent = scene,
					position = position,
					model = 'assets/block.obj',
					origin_y = 0.5,
					texture = texture,
					color = color.color(0,0,random.uniform(0.9,1)),
					scale = 0.5)

			def input(self,key):
				if self.hovered:
					if key == 'right mouse down':
						punch_sound.play()
						if block_pick == 1: voxel = Voxel(position = self.position + mouse.normal, texture = grass_texture)
						if block_pick == 2: voxel = Voxel(position = self.position + mouse.normal, texture = stone_texture)
						if block_pick == 3: voxel = Voxel(position = self.position + mouse.normal, texture = brick_texture)
						if block_pick == 4: voxel = Voxel(position = self.position + mouse.normal, texture = dirt_texture)

					if key == 'left mouse down':
						punch_sound.play()
						destroy(self)

		class Sky(Entity):
			def __init__(self):
				super().__init__(
					parent = scene,
					model = 'sphere',
					texture = sky_texture,
					scale = 150,
					double_sided = True)

		class Hand(Entity):
			def __init__(self):
				super().__init__(
					parent = camera.ui,
					model = 'assets/arm',
					texture = arm_texture,
					scale = 0.2,
					rotation = Vec3(150,-10,0),
					position = Vec2(0.4,-0.6))

			def active(self):
				self.position = Vec2(0.3,-0.5)

			def notActive(self):
				self.position = Vec2(0.4,-0.6)

		player = FirstPersonController()
		player.jump_height = 1.5
		sky = Sky()
		hand = Hand()

		for z in range(20):
			for x in range(20):
				for y in range(2):
					voxel = Voxel(position = (x,y,z))


			time.sleep(1)
		app.run()

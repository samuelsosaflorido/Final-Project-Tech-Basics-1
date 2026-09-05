# For this part I have used this video which I found really useful :) https://www.youtube.com/watch?v=1q_0l71Ln7I
# Nevertheless did not implement most of the stuff because it is mainly for adventure games in which the inventory plays a huge role, like for selling items even
# I used also the design of the yard for this but we can change it

import pygame

# You can add more items here :) 
ALL_ITEMS = [
    "Key Fragment 1",
    "Key Fragment 2",
    "Key Fragment 3",
    "Strange Key",
    "Medication Fragment 1",
    "Medication Fragment 2",
    "Medication Fragment 3",
    "Medication",
    "Strange Note 1",
    "Strange Note 2",
    "Strange Note 3",
    "Spade"
]

class Inventory:
    def __init__(self, max_slots=8):
        self.max_slots = max_slots
        self.items = []
        self.selected_idx = 0

        # Color palette for the inventory
        self.color_bg = (15, 10, 15)
        self.color_border = (140, 30, 30)      # COLOR_BLOOD
        self.color_bone = (230, 225, 210)
        self.color_slot = (25, 20, 28)
        self.color_selected = (200, 180, 120)
        self.color_hint = (150, 145, 140)

    def add_item(self, item):
        if len(self.items) < self.max_slots:
            self.items.append(item)
            self.combine()
            return True
        return False

    def get_index(self, item):
        for index, slot in enumerate(self.items):
            if slot == item:
                return index
        return -1

    def get_selected_item(self):
        if 0 <= self.selected_idx < len(self.items):
            return self.items[self.selected_idx]
        return None

    def use_selected(self):
        if self.selected_idx < len(self.items):
            item = self.items[self.selected_idx]
            if item != "Spade" and not item.startswith("Strange Note"):
                return self.items.pop(self.selected_idx)
            return item
        return None

    def move_selection(self, direction):
        self.selected_idx = (self.selected_idx + direction) % self.max_slots

    def combine(self):
        meds_frags = ["Medication Fragment 1", "Medication Fragment 2", "Medication Fragment 3"]
        if all(frag in self.items for frag in meds_frags):
            for frag in meds_frags:
                self.items.remove(frag)
            self.items.append("Medication")

        keys = ["Key Fragment 1", "Key Fragment 2", "Key Fragment 3"]
        if all(frag in self.items for frag in keys):
            for frag in keys:
                self.items.remove(frag)
            self.items.append("Strange Key")

    # This is just temporary maybe we need to fix this once we create the inventory file
    def draw(self, screen, font, small_font):
        window_width = screen.get_width()
        window_height = screen.get_height()

        # This renders the entire inventory which maybe we can use as the basis for the ivnentory file
        overlay = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
        overlay.fill((6, 4, 8, 225))
        screen.blit(overlay, (0, 0))

        # This defines how big is the main menu for the inventory
        panel_w, panel_h = 680, 240
        panel_x = (window_width - panel_w) // 2
        panel_y = (window_height - panel_h) // 2
        panel_rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)

        pygame.draw.rect(screen, (15, 10, 15), panel_rect, border_radius=6)
        pygame.draw.rect(screen, self.color_border, panel_rect, 2, border_radius=6)

        title_surf = font.render("INVENTORY / POCKETS", True, self.color_bone)
        screen.blit(title_surf, (panel_x + 20, panel_y + 15))

        slot_size, gap = 50, 12
        start_x, start_y = panel_x + 25, panel_y + 50

        # This is a conditional loop to create 8 slots for the inventory
        # Each slot has its corresponding coordinate for it to make sense 
        for i in range(8):
            col, row = i % 4, i // 4
            sx = start_x + col * (slot_size + gap)
            sy = start_y + row * (slot_size + gap)
            slot_rect = pygame.Rect(sx, sy, slot_size, slot_size)

            if i == self.selected_idx:
                pygame.draw.rect(screen, (60, 15, 20), slot_rect, border_radius=4)
                pygame.draw.rect(screen, self.color_selected, slot_rect, 2, border_radius=4)
            else:
                pygame.draw.rect(screen, (25, 20, 25), slot_rect, border_radius=4)
                pygame.draw.rect(screen, (80, 75, 70), slot_rect, 1, border_radius=4)

            if i < len(self.items):
                short_name = self.items[i][:4].upper()
                name_surf = small_font.render(short_name, True, self.color_bone)
                screen.blit(name_surf, (sx + 6, sy + 18))

        # Right details panel
        desc_x, desc_y, desc_w, desc_h = panel_x + 285, panel_y + 50, 365, 120
        pygame.draw.rect(screen, (10, 8, 12), (desc_x, desc_y, desc_w, desc_h), border_radius=4)
        pygame.draw.rect(screen, (50, 40, 45), (desc_x, desc_y, desc_w, desc_h), 1, border_radius=4)

        # This is basically when the player obtains a valid object
        # It obtains the name of it and renders the name
        if 0 <= self.selected_idx < len(self.items):
            item_name = self.items[self.selected_idx]
            item_title = font.render(item_name, True, self.color_selected)
            screen.blit(item_title, (desc_x + 12, desc_y + 10))

            if "Strange Note" in item_name:
                act_surf = small_font.render("[Press E to read Note]", True, (120, 200, 140))
                screen.blit(act_surf, (desc_x + 12, desc_y + desc_h - 22))
        else:
            empty_surf = small_font.render("Empty Slot", True, (100, 95, 95))
            screen.blit(empty_surf, (desc_x + 12, desc_y + 12))  # This is when the slot is completely empty, so it shows it with the gray color

        controls_surf = small_font.render("[ARROWS] Select Slot | [TAB / ESC] Close", True, (140, 135, 130))
        screen.blit(controls_surf, (panel_x + 20, panel_y + panel_h - 22))

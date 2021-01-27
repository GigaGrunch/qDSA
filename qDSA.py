import sys
import json
from argparse import ArgumentParser
from PySide2.QtWidgets import *
from PySide2.QtCore import *


argument_parser = ArgumentParser()
argument_parser.add_argument("character_json_file", type=str)
arguments = argument_parser.parse_args()
character_json_file = arguments.character_json_file


app = QApplication(sys.argv)
main_widget = QWidget()
main_layout = QVBoxLayout()
main_widget.setLayout(main_layout)
current_layout = main_layout
parent_layouts = []



def toggle_sub_widget(button, widget):
	if button.isChecked():
		widget.show()
	else:
		widget.hide()

def begin_sub_widget(name: str):
	global current_layout
	sub_widget = QWidget()
	vertical_layout = QVBoxLayout()
	sub_widget.setLayout(vertical_layout)

	toggle_button = QPushButton(name)
	toggle_button.setCheckable(True)
	toggle_button.toggle()
	toggle_button.clicked.connect(lambda: toggle_sub_widget(toggle_button, sub_widget))
	current_layout.addWidget(toggle_button)
	current_layout.addWidget(sub_widget)

	parent_layouts.append(current_layout)
	current_layout = vertical_layout

def begin_horizontal():
	global current_layout, parent_layouts
	horizontal_layout = QHBoxLayout()
	current_layout.insertLayout(-1, horizontal_layout)
	parent_layouts.append(current_layout)
	current_layout = horizontal_layout

def begin_vertical():
	global current_layout, parent_layouts
	vertical_layout = QVBoxLayout()
	current_layout.insertLayout(-1, vertical_layout)
	parent_layouts.append(current_layout)
	current_layout = vertical_layout

def begin_table(columnCount: int, title=None, headers=None):
	global current_layout, parent_layouts

	begin_vertical()

	if (title is not None):
		label(title)

	table = QTableWidget()
	table.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
	table.setColumnCount(columnCount)
	if headers == None:
		table.horizontalHeader().hide()
	else:
		table.setHorizontalHeaderLabels(headers)
	table.verticalHeader().hide()
	table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
	current_layout.addWidget(table)
	end_layout()

	parent_layouts.append(current_layout)
	current_layout = table

def end_layout():
	global current_layout, parent_layouts
	current_layout = parent_layouts[-1]
	del(parent_layouts[-1])

def label(text: str, alignment = Qt.AlignCenter):
	global current_layout
	label = QLabel(text, alignment=alignment)
	label.setMargin(5)
	return label

def attribute(name: str, value: int):
	attribute_label = label("{}\n{}".format(name, value))
	current_layout.addWidget(attribute_label)

def talent(name: str, attributes, value: int):
	global current_layout

	name_label = label(name, alignment=Qt.AlignLeft)
	attributes_label = label("{} • {} • {}"
		.format(attributes[0], attributes[1], attributes[2]))
	value_label = label(str(value))

	row = current_layout.rowCount()
	current_layout.setRowCount(row + 1)

	current_layout.setCellWidget(row, 0, name_label)
	current_layout.setCellWidget(row, 1, attributes_label)
	current_layout.setCellWidget(row, 2, value_label)
	current_layout.resizeColumnsToContents()

def advantage(name: str, text: str):
	global current_layout

	name_label = label(name, alignment=Qt.AlignLeft)
	text_label = label(text)

	row = current_layout.rowCount()
	current_layout.setRowCount(row + 1)
	current_layout.setCellWidget(row, 0, name_label)
	current_layout.setCellWidget(row, 1, text_label)
	current_layout.resizeColumnsToContents()

def weapon(name: str, object):
	global current_layout

	name_label = label(name, alignment=Qt.AlignLeft)
	at_label = label(str(object["AT"]))
	pa_label = label(str(object["PA"]))
	tp_label = label(str(object["TP"]))

	row = current_layout.rowCount()
	current_layout.setRowCount(row + 1)

	current_layout.setCellWidget(row, 0, name_label)
	current_layout.setCellWidget(row, 1, at_label)
	current_layout.setCellWidget(row, 2, pa_label)
	current_layout.setCellWidget(row, 3, tp_label)
	current_layout.resizeColumnsToContents()


def spell(name: str, object):
	global current_layout

	name_label = label(name, alignment=Qt.AlignLeft)
	attributes = object["attributes"]
	attributes_label = label("{} • {} • {}"
		.format(attributes[0], attributes[1], attributes[2]))
	value_label = label(str(object["value"]))
	cost_label = label(object["cost"])
	cast_time_label = label(str(object["cast_time"]))
	range_label = label(str(object["range"]))
	duration_label = label(str(object["duration"]))
	text_label = label(object["text"], alignment=Qt.AlignLeft)

	row = current_layout.rowCount()
	current_layout.setRowCount(row + 1)

	current_layout.setCellWidget(row, 0, name_label)
	current_layout.setCellWidget(row, 1, attributes_label)
	current_layout.setCellWidget(row, 2, value_label)
	current_layout.setCellWidget(row, 3, cost_label)
	current_layout.setCellWidget(row, 4, cast_time_label)
	current_layout.setCellWidget(row, 5, range_label)
	current_layout.setCellWidget(row, 6, duration_label)
	current_layout.setCellWidget(row, 7, text_label)
	current_layout.resizeColumnsToContents()


with open(character_json_file) as file:
	character_file_text = file.read()
character_json = json.loads(character_file_text)

with open(character_json_file + ".backup", "w") as backup_file:
	backup_file.write(character_file_text)



# character name
if "name" in character_json:
	name_label = label(character_json["name"])
	current_layout.addWidget(name_label)


# attributes
if "attributes" in character_json:
	begin_horizontal()
	current_layout.addStretch()
	for attribute_key, attribute_value in character_json["attributes"].items():
		attribute(attribute_key, attribute_value)
	current_layout.addStretch()
	end_layout()


# inventory
def change_item_amount(name, amount):
	global character_json_file

	character_json["inventory"][name] = amount
	with open(character_json_file, "w") as file:
		text = json.dumps(character_json, indent="\t", ensure_ascii=False)
		file.write(text)

if "inventory" in character_json:
	begin_sub_widget("Inventar")
	begin_table(2)

	money = character_json["inventory"]["money"]
	remainder = money
	k = money % 10
	remainder -= k
	h = (remainder / 10) % 10
	remainder -= (h * 10)
	s = (remainder / 100) % 10
	remainder -= (s * 100)
	d = (remainder / 1000)
	remainder -= (d * 1000)

	if remainder != 0:
		print("Money calculation failure!")
		exit(1)

	def money_spinbox(label, initial_value):
		label = QLabel(label, margin=5)
		spinbox = QSpinBox()
		spinbox.setMaximum(999999)
		spinbox.setValue(initial_value)

		row = current_layout.rowCount()
		current_layout.setRowCount(row + 1)
		current_layout.setCellWidget(row, 0, label)
		current_layout.setCellWidget(row, 1, spinbox)

		return spinbox

	d_spinbox = money_spinbox("Dukaten", d)
	s_spinbox = money_spinbox("Silbertaler", s)
	h_spinbox = money_spinbox("Heller", h)
	k_spinbox = money_spinbox("Kreuzer", k)

	def update_money():
		change_item_amount("money",
			k_spinbox.value() +
			h_spinbox.value() *   10 +
			s_spinbox.value() *  100 +
			d_spinbox.value() * 1000)

	k_spinbox.valueChanged.connect(lambda: update_money())
	h_spinbox.valueChanged.connect(lambda: update_money())
	s_spinbox.valueChanged.connect(lambda: update_money())
	d_spinbox.valueChanged.connect(lambda: update_money())

	current_layout.resizeColumnsToContents()
	end_layout()
	end_layout()


# advantages
if "advantages" in character_json:
	begin_sub_widget("Vorteile / Nachteile")
	begin_table(2)
	for advantage_key, advantage_value in character_json["advantages"].items():
		advantage(advantage_key, advantage_value)
	end_layout()
	end_layout()



# talents
if "talents" in character_json:
	begin_sub_widget("Talente")
	talent_index = 0
	for talent_header, talents_object in character_json["talents"].items():
		if talent_index % 2 == 0:
			begin_horizontal()

		begin_table(3, talent_header)
		for talent_key, talent_object in talents_object.items():
			talent(talent_key, talent_object["attributes"], talent_object["value"])
		end_layout()

		if talent_index % 2 == 1:
			end_layout()

		talent_index += 1

	current_layout.addStretch()
	end_layout()
	end_layout()

# combat
if "combat" in character_json:
	begin_sub_widget("Kampf")
	begin_horizontal()
	current_layout.addStretch()
	for base_key, base_value in character_json["combat"]["base"].items():
		attribute(base_key, base_value)
	current_layout.addStretch()
	end_layout()

	begin_table(4, headers=["Waffe", "AT", "PA", "TP"])
	for weapon_key, weapon_object in character_json["combat"]["weapons"].items():
		weapon(weapon_key, weapon_object)
	end_layout()
	end_layout()

# spells
if "spells" in character_json:
	begin_sub_widget("Magie")
	begin_table(8, headers=["Zauber", "Probe", "FW", "Kosten", "Zauberdauer", "Reichweite", "Wirkungsdauer", "Beschreibung"])
	for spell_key, spell_object in character_json["spells"].items():
		spell(spell_key, spell_object)
	end_layout()
	end_layout()


main_layout.addStretch()

main_widget.show()
sys.exit(app.exec_())

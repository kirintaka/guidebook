import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry
import sqlite3

def get_plants_names():
    conn = sqlite3.connect('guidebook.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id_plant, plant_name FROM plants where is_deleted=0')
    plants_names = {row[1]: row[0] for row in cursor.fetchall()}

    conn.close()
    return plants_names

class GuideBook(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('1300x700')
        self.title("Medicine Guide Book")
        self.create_widgets()

    def create_widgets(self):
        title_label = ttk.Label(self, text="Medicine Guide Book", font=("Helvetica", 16))
        title_label.grid(row=0, column=0, columnspan=1, pady=10)

        dictionary_label = ttk.Label(self, text="Выберите справочник:")
        dictionary_label.grid(row=1, column=0, columnspan=1, pady=10)

        self.dictionary_var = tk.StringVar()
        dictionary_combobox = ttk.Combobox(self, textvariable=self.dictionary_var, values=["plants", "medicines"])
        dictionary_combobox.grid(row=2, column=0, columnspan=1, pady=10)

        view_button = ttk.Button(self, text="Просмотреть данные", command=self.view_data)
        view_button.grid(row=3, column=0, columnspan=1, pady=10)
        
        self.data_tree = ttk.Treeview(self, columns=(1, 2, 3, 4, 5, 6, 7, 8, 9), show="headings", height=12)
        self.data_tree.grid(row=4, column=0, sticky='nsew')

        data_scroll = ttk.Scrollbar(self, orient='vertical', command=self.data_tree.yview)
        column_scroll = ttk.Scrollbar(self, orient='horizontal', command=self.data_tree.xview)
        self.data_tree.configure(xscrollcommand=column_scroll.set, yscrollcommand=data_scroll.set)
        data_scroll.grid(row=4, column=1, sticky='ns')
        column_scroll.grid(row=5, column=0, sticky="ew")
        
        edit_button = ttk.Button(self, text="Редактировать данные", command=self.edit_data)
        edit_button.grid(row=6, column=0, columnspan=1, pady=10)

        add_button = ttk.Button(self, text="Добавить данные", command=self.add_data)
        add_button.grid(row=7, column=0, columnspan=1, pady=10)

        delete_button = ttk.Button(self, text="Удалить данные", command=self.delete_data)
        delete_button.grid(row=8, column=0, columnspan=1, pady=10)
        
        name_label = ttk.Label(self, text="Жалова Дарья Александровна, 4 курс, 4 группа, 2023 год")
        name_label.grid(row=9, column=0, pady=10, padx=10)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
            
    
    def view_data(self):
        selected_dictionary = self.dictionary_var.get()

        if not selected_dictionary:
            return

        conn = sqlite3.connect('guidebook.db')
        cursor = conn.cursor()

        cursor.execute(f'SELECT * FROM {selected_dictionary} WHERE is_deleted=0')
        if selected_dictionary == "plants":
            columns = [(1, "Название растения"), (2, "Научное название"), (3, "Свойства"), (4, "Сезон сбора")]
            for col, col_name in columns:
              self.data_tree.heading(col, text=col_name, command=lambda c=col: self.sort_column(c, "plants"))
            cursor.execute(f'SELECT plant_name, scientific_name, properties, harvest_season FROM {selected_dictionary} WHERE is_deleted=0')
            

        if selected_dictionary == "medicines":
            columns = [(1, "Название препарата"), (2, "Активный компонент"), (3, "Используемое растение"), (4, "Описание"), (5, "Способ применения" ), (6, "Дозировка"), (7, "Дата производства"), (8, "Срок годности"), (9, "Цена")]
            for col, col_name in columns:
              self.data_tree.heading(col, text=col_name, command=lambda c=col: self.sort_column(c, "medicines"))
            cursor.execute(f'''
                            SELECT
                                medicine_name, active_component,
                                plants.plant_name,
                                description, application_methods, dosage,
                                strftime('%d-%m-%Y', manufacturing_date),
                                strftime('%d-%m-%Y', expiration_date),
                                cost
                            FROM {selected_dictionary}
                            LEFT JOIN plants ON {selected_dictionary}.plant_ids = plants.id_plant
                            WHERE {selected_dictionary}.is_deleted = 0
                        '''
                           )
            
        data = cursor.fetchall()

        conn.close()

        for i in self.data_tree.get_children():
            self.data_tree.delete(i)

        for row in data:
            self.data_tree.insert("", "end", values=row)
            
    def sort_column(self, col, selected_dictionary):
        data = [(self.data_tree.set(item, col), item) for item in self.data_tree.get_children('')]

        if (col in (1, 2, 4) and selected_dictionary == "plants") or (col in (1, 4, 5, 6, 7, 8, 9) and selected_dictionary == "medicines"):  # Колонки с датой и строкой
          data.sort(key=lambda x: (self.get_type(x[0]), x[0]))
        else:
          data.sort(key=lambda x: (float(x[0]) if type(x[0]) != str else x[0]) if x[0] != 'NULL' else float('inf'))

        for index, (val, item) in enumerate(data):
          self.data_tree.move(item, '', index)

    def get_type(self, value):
        if value == 'NULL':
          return 3
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return 0  # Дата
        except ValueError:
            try:
                float(value)
                return 1  # Число
            except ValueError:
                return 2  # Строка
            
    def add_data(self):
        selected_dictionary = self.dictionary_var.get()

        add_window = tk.Toplevel(self)
        add_window.title("Добавить данные")
        if selected_dictionary == "plants":
          name_label = ttk.Label(add_window, text="Название растения:")
          name_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
          name_entry = ttk.Entry(add_window)
          name_entry.grid(row=0, column=1, padx=10, pady=5)
          
          scientific_label = ttk.Label(add_window, text="Научное название:")
          scientific_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
          scientific_entry = ttk.Entry(add_window)
          scientific_entry.grid(row=1, column=1, padx=10, pady=5)

          properties_label = ttk.Label(add_window, text="Свойства:")
          properties_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
          properties_entry = ttk.Entry(add_window)
          properties_entry.grid(row=2, column=1, padx=10, pady=5)

          season_label = ttk.Label(add_window, text="Сезон сбора:")
          season_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
          season_entry = ttk.Entry(add_window)
          season_entry.grid(row=3, column=1, padx=10, pady=5)
          
        if selected_dictionary == "medicines":
          name_label = ttk.Label(add_window, text="Название препарата:")
          name_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
          name_entry = ttk.Entry(add_window)
          name_entry.grid(row=0, column=1, padx=10, pady=5)

          component_label = ttk.Label(add_window, text="Активный компонент:")
          component_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
          component_entry = ttk.Entry(add_window)
          component_entry.grid(row=1, column=1, padx=10, pady=5)

          plants_label = ttk.Label(add_window, text="Используемые растения:")
          plants_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
          plants_names = get_plants_names()
          plants_combobox = ttk.Combobox(add_window)
          plants_combobox['values'] = list(plants_names.keys())
          plants_combobox.grid(row=2, column=1, padx=10, pady=5)

          description_label = ttk.Label(add_window, text="Описание препарата:")
          description_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
          description_entry = ttk.Entry(add_window)
          description_entry.grid(row=3, column=1, padx=10, pady=5)
          
          application_label = ttk.Label(add_window, text="Способы применения:")
          application_label.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
          application_entry = ttk.Entry(add_window)
          application_entry.grid(row=4, column=1, padx=10, pady=5)
          
          doze_label = ttk.Label(add_window, text="Дозировка:")
          doze_label.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)
          doze_entry = ttk.Entry(add_window)
          doze_entry.grid(row=5, column=1, padx=10, pady=5)
          
          maded_label = ttk.Label(add_window, text="Срок изготовления:")
          maded_label.grid(row=6, column=0, padx=10, pady=5, sticky=tk.W)
          maded_entry = DateEntry(add_window, date_pattern="yyyy-mm-dd")
          maded_entry.grid(row=6, column=1, padx=10, pady=5)
          
          expiration_label = ttk.Label(add_window, text="Срок годности:")
          expiration_label.grid(row=7, column=0, padx=10, pady=5, sticky=tk.W)
          expiration_entry = DateEntry(add_window, date_pattern="yyyy-mm-dd")
          expiration_entry.grid(row=7, column=1, padx=10, pady=5)
          
          cost_label = ttk.Label(add_window, text="Стоимость:")
          cost_label.grid(row=8, column=0, padx=10, pady=5, sticky=tk.W)
          cost_entry = ttk.Entry(add_window)
          cost_entry.grid(row=8, column=1, padx=10, pady=5)
          
          

        def add_new_entry():
           if selected_dictionary == "plants":
            new_name = name_entry.get()
            new_scientific = scientific_entry.get()
            new_properties = properties_entry.get()
            new_season = season_entry.get()
            
 
            if not new_name or not new_scientific or not new_season:
                messagebox.showwarning("Ошибка", "Заполните все поля")
                return
            if new_properties.lower() == 'null' or new_properties.lower() == '' or new_properties.lower() == ' ' or new_properties.lower() == 'none':
              new_season = 'NULL'
            
            
            conn = sqlite3.connect('guidebook.db')
            cursor = conn.cursor()

            cursor.execute(f'''
                SELECT * FROM {selected_dictionary} 
                WHERE plant_name=? AND is_deleted=1
                ''', (new_name,))
            existing_deleted_entry = cursor.fetchone()

            if existing_deleted_entry:
              cursor.execute(f'''
                UPDATE {selected_dictionary} 
                SET scientific_name=?, properties=?, harvest_season=?, is_deleted=0
                WHERE id_plant=?
                ''', (new_scientific, new_properties, new_season, existing_deleted_entry[0]))
            else:
              cursor.execute(f'''
               INSERT INTO {selected_dictionary} (plant_name, scientific_name, properties, harvest_season, is_deleted)
               VALUES (?, ?, ?, ?, 0)
               ''', (new_name, new_scientific, new_properties, new_season))

            conn.commit()
            conn.close()

            self.view_data()
            add_window.destroy()
            

           if selected_dictionary == "medicines":
            new_name = name_entry.get()
            new_component = component_entry.get()
            new_plant = plants_combobox.get()
            new_plant_id = plants_names[new_plant]
            new_description = description_entry.get()
            new_application = application_entry.get()
            new_doze = doze_entry.get()
            new_maded = maded_entry.get()
            new_expiration = expiration_entry.get()
            new_cost = cost_entry.get()           

            if not new_name or not new_plant or not new_description or not new_application \
              or not new_doze or not new_maded or not new_expiration or not new_cost:
                messagebox.showwarning("Ошибка", "Заполните все поля")
                return
            
            if new_component.lower() == 'null' or new_component.lower() == '' or new_component.lower() == ' ' or new_component.lower() == 'none':
              new_component = "NULL"
              
            try:
              new_doze = float(new_doze)
            except ValueError:
              messagebox.showwarning("Ошибка", "Неверный формат дозировки (должно быть число)")
              return
         
            try:
                new_cost = float(new_cost)
            except ValueError:
                messagebox.showwarning("Ошибка", "Неверный формат цены (должно быть число)")
                return 

            conn = sqlite3.connect('guidebook.db')
            cursor = conn.cursor()


            try:
              new_maded = datetime.strptime(new_maded, "%Y-%m-%d").date()
            except ValueError:
              messagebox.showwarning("Ошибка", "Неверный формат даты изготовления")
              conn.close()
              
            try:
              new_expiration = datetime.strptime(new_expiration, "%Y-%m-%d").date()
            except ValueError:
              messagebox.showwarning("Ошибка", "Неверный формат срока годности")
              conn.close()


            cursor.execute(f'''
                SELECT * FROM {selected_dictionary} 
                WHERE medicine_name=? AND is_deleted=1
                ''', (new_name,))
            existing_deleted_entry = cursor.fetchone()

            if existing_deleted_entry:
              cursor.execute(f'''
                UPDATE {selected_dictionary} 
                SET active_component=?, plant_ids=?, description=?, application_methods = ?, dosage = ?, manufacturing_date = ?, expiration_date = ?, cost = ?, is_deleted=0
                WHERE id_medicine=?
                ''', (new_component, new_plant_id, new_description, new_application, new_doze, new_maded, new_expiration, new_cost, existing_deleted_entry[0]))
            else:
              cursor.execute(f'''
                INSERT INTO {selected_dictionary} (medicine_name, active_component, plant_ids, description, application_methods, dosage, manufacturing_date, expiration_date, cost, is_deleted)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
                ''', (new_name, new_component, new_plant_id, new_description, new_application, new_doze, new_maded, new_expiration, new_cost))
              
            conn.commit()
            conn.close()

            self.view_data()

            add_window.destroy()
        add_button = ttk.Button(add_window, text="Добавить", command=add_new_entry)
        add_button.grid(row=10, column=0, columnspan=2, pady=10)
    
    def delete_data(self):
        selected_dictionary = self.dictionary_var.get()
        selected_item = self.data_tree.selection()

        if not selected_item:
            messagebox.showwarning("Ошибка", "Выберите запись для удаления")
            return

        confirm = messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить выбранную запись?")
        
        if confirm:

            conn = sqlite3.connect('guidebook.db')
            cursor = conn.cursor()
            if selected_dictionary == "medicines":
               cursor.execute(f'UPDATE {selected_dictionary} SET is_deleted=1 WHERE medicine_name=?', (self.data_tree.item(selected_item, 'values')[0],))
            if selected_dictionary == "plants":
               cursor.execute(f'UPDATE {selected_dictionary} SET is_deleted=1 WHERE plant_name=?', (self.data_tree.item(selected_item, 'values')[0],))

            conn.commit()
            conn.close()

            self.view_data()

    def edit_data(self):
        selected_dictionary = self.dictionary_var.get()
        selected_item = self.data_tree.selection()

        if not selected_item:
            messagebox.showwarning("Ошибка", "Выберите запись для редактирования")
            return

        edit_window = tk.Toplevel(self)
        edit_window.title("Редактировать данные")

        selected_data = self.data_tree.item(selected_item, 'values')

        if selected_dictionary == "plants":

          name_label = ttk.Label(edit_window, text="Название растения:")
          name_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
          name_entry = ttk.Entry(edit_window)
          name_entry.grid(row=0, column=1, padx=10, pady=5)
          name_entry.insert(0, selected_data[0])

          scientific_label = ttk.Label(edit_window, text="Научное название:")
          scientific_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
          scientific_entry = ttk.Entry(edit_window)
          scientific_entry.grid(row=1, column=1, padx=10, pady=5)
          scientific_entry.insert(0, selected_data[1])

          properties_label = ttk.Label(edit_window, text="Свойства:")
          properties_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
          properties_entry = ttk.Entry(edit_window)
          properties_entry.grid(row=2, column=1, padx=10, pady=5)
          properties_entry.insert(0, selected_data[2])

          season_label = ttk.Label(edit_window, text="Сезон сбора:")
          season_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
          season_entry = ttk.Entry(edit_window)
          season_entry.grid(row=3, column=1, padx=10, pady=5)
          season_entry.insert(0, selected_data[3])
          ##########################################################################################################
        if selected_dictionary == "medicines":
          name_label = ttk.Label(edit_window, text="Название препарата:")
          name_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
          name_entry = ttk.Entry(edit_window)
          name_entry.grid(row=0, column=1, padx=10, pady=5)
          name_entry.insert(0, selected_data[0])

          component_label = ttk.Label(edit_window, text="Активный компонент:")
          component_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
          component_entry = ttk.Entry(edit_window)
          component_entry.grid(row=1, column=1, padx=10, pady=5)
          component_entry.insert(0, selected_data[1])

          plants_label = ttk.Label(edit_window, text="Используемые растения:")
          plants_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
          plants_names = get_plants_names()
          plants_combobox = ttk.Combobox(edit_window)
          plants_combobox['values'] = list(plants_names.keys())
          plants_combobox.grid(row=2, column=1, padx=10, pady=5)
          plants_combobox.insert(0, selected_data[2])

          description_label = ttk.Label(edit_window, text="Описание препарата:")
          description_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
          description_entry = ttk.Entry(edit_window)
          description_entry.grid(row=3, column=1, padx=10, pady=5)
          description_entry.insert(0, selected_data[3])
          
          application_label = ttk.Label(edit_window, text="Способы применения:")
          application_label.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
          application_entry = ttk.Entry(edit_window)
          application_entry.grid(row=4, column=1, padx=10, pady=5)
          application_entry.insert(0, selected_data[4])


          doze_label = ttk.Label(edit_window, text="Дозировка:")
          doze_label.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)
          doze_entry = ttk.Entry(edit_window)
          doze_entry.grid(row=5, column=1, padx=10, pady=5)
          doze_entry.insert(0, selected_data[5])
          
          maded_label = ttk.Label(edit_window, text="Срок изготовления:")
          maded_label.grid(row=6, column=0, padx=10, pady=5, sticky=tk.W)
          maded_entry = DateEntry(edit_window, date_pattern="yyyy-mm-dd")
          maded_entry.grid(row=6, column=1, padx=10, pady=5)

          expiration_label = ttk.Label(edit_window, text="Срок годности:")
          expiration_label.grid(row=7, column=0, padx=10, pady=5, sticky=tk.W)
          expiration_entry = DateEntry(edit_window, date_pattern="yyyy-mm-dd")
          expiration_entry.grid(row=7, column=1, padx=10, pady=5)

          cost_label = ttk.Label(edit_window, text="Стоимость:")
          cost_label.grid(row=8, column=0, padx=10, pady=5, sticky=tk.W)
          cost_entry = ttk.Entry(edit_window)
          cost_entry.grid(row=8, column=1, padx=10, pady=5)
          cost_entry.insert(0, selected_data[8])


        def save_changes():
           if selected_dictionary == "medicines":
            new_name = name_entry.get()
            new_component = component_entry.get()
            new_plant = plants_combobox.get()
            new_plant_id = plants_names[new_plant]
            new_description = description_entry.get()
            new_application = application_entry.get()
            new_doze = doze_entry.get()
            new_maded = maded_entry.get()
            new_expiration = expiration_entry.get()
            new_cost = cost_entry.get()  

            if not new_name or not new_plant or not new_description or not new_application \
              or not new_doze or not new_maded or not new_expiration or not new_cost:
                messagebox.showwarning("Ошибка", "Заполните все поля")
                return
            
            if new_component.lower() == 'null' or new_component.lower() == '' or new_component.lower() == ' ' or new_component.lower() == 'none':
              new_component = "NULL"
              
            try:
              new_doze = float(new_doze)
            except ValueError:
              messagebox.showwarning("Ошибка", "Неверный формат дозировки (должно быть число)")
              return
         
            try:
                new_cost = float(new_cost)
            except ValueError:
                messagebox.showwarning("Ошибка", "Неверный формат цены (должно быть число)")
                return  

            conn = sqlite3.connect('guidebook.db')
            cursor = conn.cursor()

            try:
              new_maded = datetime.strptime(new_maded, "%Y-%m-%d").date()
            except ValueError:
              messagebox.showwarning("Ошибка", "Неверный формат даты изготовления")
              conn.close()
              
            try:
              new_expiration = datetime.strptime(new_expiration, "%Y-%m-%d").date()
            except ValueError:
              messagebox.showwarning("Ошибка", "Неверный формат срока годности")
              conn.close()

            cursor.execute(f'''
                UPDATE {selected_dictionary} 
                SET medicine_name=?, active_component=?, plant_ids=?, description=?, application_methods = ?, dosage = ?, manufacturing_date = ?, expiration_date = ?, cost = ?
                WHERE medicine_name=?
                ''', (new_name, new_component, new_plant_id, new_description, new_application, new_doze, new_maded, new_expiration, new_cost, selected_data[0]))

            conn.commit()
            conn.close()

            self.view_data()

            edit_window.destroy()
     #######################################################################################
           if selected_dictionary == "plants":
            new_name = name_entry.get()
            new_scientific = scientific_entry.get()
            new_properties = properties_entry.get()
            new_season = season_entry.get()

            if not new_name or not new_scientific or not new_season:
                messagebox.showwarning("Ошибка", "Заполните все поля")
                return
            if new_properties.lower() == 'null' or new_properties.lower() == '' or new_properties.lower() == ' ' or new_properties.lower() == 'none':
              new_season = 'NULL'
            

            conn = sqlite3.connect('guidebook.db')
            cursor = conn.cursor()

            cursor.execute(f'''
                UPDATE {selected_dictionary} 
                SET plant_name=?, scientific_name=?, properties=?, harvest_season=?
                WHERE plant_name=?
                ''', (new_name, new_scientific, new_properties, new_season, selected_data[0]))

            conn.commit()
            conn.close()

            self.view_data()

            edit_window.destroy()

        save_button = ttk.Button(edit_window, text="Сохранить", command=save_changes)
        save_button.grid(row=10, column=0, columnspan=2, pady=10)


if __name__ == "__main__":
    app = GuideBook()
    app.mainloop()
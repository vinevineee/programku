import json
import os
from datetime import datetime

# File untuk menyimpan data to do list
TODO_FILE = "todos.json"

class TodoList:
    def __init__(self):
        self.todos = self.load_todos()
    
    def load_todos(self):
        """Memuat to do list dari file JSON"""
        if os.path.exists(TODO_FILE):
            with open(TODO_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    
    def save_todos(self):
        """Menyimpan to do list ke file JSON"""
        with open(TODO_FILE, "w", encoding="utf-8") as f:
            json.dump(self.todos, f, ensure_ascii=False, indent=2)
    
    def add_todo(self, task):
        """Menambah tugas baru"""
        todo = {
            "id": len(self.todos) + 1,
            "task": task,
            "status": "Belum Selesai",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.todos.append(todo)
        self.save_todos()
        print(f"✓ Tugas '{task}' berhasil ditambahkan!")
    
    def view_todos(self):
        """Menampilkan semua tugas"""
        if not self.todos:
            print("\n📭 Tidak ada tugas. Tambahkan tugas baru!\n")
            return
        
        print("\n" + "="*70)
        print(f"{'ID':<5} {'Tugas':<35} {'Status':<15} {'Dibuat':<15}")
        print("="*70)
        
        for todo in self.todos:
            status_icon = "✓" if todo["status"] == "Selesai" else "○"
            print(f"{todo['id']:<5} {todo['task']:<35} {status_icon} {todo['status']:<12} {todo['created_at']:<15}")
        
        print("="*70 + "\n")
    
    def mark_complete(self, todo_id):
        """Menandai tugas sebagai selesai"""
        for todo in self.todos:
            if todo["id"] == todo_id:
                if todo["status"] == "Selesai":
                    print(f"⚠ Tugas '{todo['task']}' sudah selesai!")
                else:
                    todo["status"] = "Selesai"
                    self.save_todos()
                    print(f"✓ Tugas '{todo['task']}' ditandai selesai!")
                return
        print(f"❌ Tugas dengan ID {todo_id} tidak ditemukan!")
    
    def delete_todo(self, todo_id):
        """Menghapus tugas"""
        for i, todo in enumerate(self.todos):
            if todo["id"] == todo_id:
                task_name = todo["task"]
                self.todos.pop(i)
                # Perbarui ID
                for j, t in enumerate(self.todos):
                    t["id"] = j + 1
                self.save_todos()
                print(f"✓ Tugas '{task_name}' berhasil dihapus!")
                return
        print(f"❌ Tugas dengan ID {todo_id} tidak ditemukan!")
    
    def update_todo(self, todo_id, new_task):
        """Mengubah tugas"""
        for todo in self.todos:
            if todo["id"] == todo_id:
                old_task = todo["task"]
                todo["task"] = new_task
                self.save_todos()
                print(f"✓ Tugas diubah dari '{old_task}' menjadi '{new_task}'!")
                return
        print(f"❌ Tugas dengan ID {todo_id} tidak ditemukan!")
    
    def show_statistics(self):
        """Menampilkan statistik to do list"""
        total = len(self.todos)
        completed = sum(1 for todo in self.todos if todo["status"] == "Selesai")
        pending = total - completed
        
        print("\n" + "="*40)
        print("📊 STATISTIK TO DO LIST")
        print("="*40)
        print(f"Total Tugas    : {total}")
        print(f"Selesai        : {completed}")
        print(f"Belum Selesai  : {pending}")
        if total > 0:
            percentage = (completed / total) * 100
            print(f"Progres        : {percentage:.1f}%")
        print("="*40 + "\n")

def main():
    """Fungsi utama untuk menjalankan aplikasi"""
    todo_list = TodoList()
    
    while True:
        print("\n╔════════════════════════════════════╗")
        print("║       📝 APLIKASI TO DO LIST       ║")
        print("╚════════════════════════════════════╝")
        print("\n1. Lihat semua tugas")
        print("2. Tambah tugas baru")
        print("3. Tandai tugas selesai")
        print("4. Ubah tugas")
        print("5. Hapus tugas")
        print("6. Lihat statistik")
        print("7. Keluar")
        
        choice = input("\nPilih menu (1-7): ").strip()
        
        if choice == "1":
            todo_list.view_todos()
        
        elif choice == "2":
            task = input("Masukkan tugas baru: ").strip()
            if task:
                todo_list.add_todo(task)
            else:
                print("❌ Tugas tidak boleh kosong!")
        
        elif choice == "3":
            todo_list.view_todos()
            try:
                todo_id = int(input("Masukkan ID tugas yang selesai: "))
                todo_list.mark_complete(todo_id)
            except ValueError:
                print("❌ Input harus berupa angka!")
        
        elif choice == "4":
            todo_list.view_todos()
            try:
                todo_id = int(input("Masukkan ID tugas yang ingin diubah: "))
                new_task = input("Masukkan tugas baru: ").strip()
                if new_task:
                    todo_list.update_todo(todo_id, new_task)
                else:
                    print("❌ Tugas tidak boleh kosong!")
            except ValueError:
                print("❌ Input harus berupa angka!")
        
        elif choice == "5":
            todo_list.view_todos()
            try:
                todo_id = int(input("Masukkan ID tugas yang ingin dihapus: "))
                todo_list.delete_todo(todo_id)
            except ValueError:
                print("❌ Input harus berupa angka!")
        
        elif choice == "6":
            todo_list.show_statistics()
        
        elif choice == "7":
            print("\n👋 Terima kasih! Sampai jumpa lagi!\n")
            break
        
        else:
            print("❌ Pilihan tidak valid! Silakan coba lagi.")

if __name__ == "__main__":
    main()

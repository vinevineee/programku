import random
import time
from enum import Enum
from typing import List, Dict, Tuple

class GameState(Enum):
    LOBBY = "LOBBY"
    TASK_PHASE = "TASK_PHASE"
    VOTING = "VOTING"
    IMPOSTOR_WIN = "IMPOSTOR_WIN"
    CREW_WIN = "CREW_WIN"
    GAME_OVER = "GAME_OVER"

class Player:
    def __init__(self, name: str, player_id: int):
        self.name = name
        self.player_id = player_id
        self.is_impostor = False
        self.is_alive = True
        self.tasks_completed = 0
        self.total_tasks = 5

    def __repr__(self):
        return f"{self.name} (ID: {self.player_id})"

class MathTask:
    def __init__(self, question: str, correct_answer: int, options: List[int]):
        self.question = question
        self.correct_answer = correct_answer
        self.options = options
        self.completed = False

    def check_answer(self, answer: int) -> bool:
        return answer == self.correct_answer

class MathQuiz:
    """Generator untuk soal-soal matematika"""
    QUESTIONS = [
        # Soal Aljabar
        ("Berapa hasil dari 2x + 5 = 13? (nilai x)", 4, [2, 3, 4, 5]),
        ("Jika 3a - 7 = 8, berapa nilai a?", 5, [3, 4, 5, 6]),
        ("Selesaikan: x + 10 = 25", 15, [10, 15, 20, 25]),
        ("Berapa x jika 2x = 16?", 8, [6, 7, 8, 9]),
        ("Jika 5x - 3 = 22, berapa nilai x?", 5, [4, 5, 6, 7]),
        
        # Soal Aritmatika
        ("Berapa hasil 15 × 4?", 60, [50, 55, 60, 65]),
        ("12 × 12 = ?", 144, [130, 140, 144, 150]),
        ("Berapa 144 ÷ 12?", 12, [10, 11, 12, 13]),
        ("99 + 101 = ?", 200, [190, 195, 200, 205]),
        ("1000 - 375 = ?", 625, [615, 620, 625, 630]),
        
        # Soal Persentase
        ("20% dari 150 adalah?", 30, [25, 28, 30, 32]),
        ("Berapa 50% dari 400?", 200, [180, 190, 200, 210]),
        ("Jika harga barang 500.000 dan diskon 10%, berapa harga akhirnya? (dalam ratusan ribu)", 45, [40, 43, 45, 50]),
        
        # Soal Geometri & Bentuk
        ("Luas persegi dengan sisi 8 cm adalah? (dalam cm²)", 64, [56, 60, 64, 72]),
        ("Keliling lingkaran dengan diameter 14 cm adalah? (gunakan π=22/7)", 44, [40, 42, 44, 46]),
        
        # Soal Barisan & Deret
        ("Berapa suku ke-5 dari barisan: 2, 4, 6, 8, ...?", 10, [8, 9, 10, 11]),
        ("Suku ke-10 dari barisan: 1, 2, 4, 8, ... (pangkat 2)?", 512, [256, 384, 512, 1024]),
        
        # Soal Logika
        ("Jika semua kucing adalah hewan, dan Misi adalah kucing, berapa kaki Misi?", 4, [2, 3, 4, 6]),
        ("Berapa jumlah sisi segitiga?", 3, [2, 3, 4, 5]),
        ("Berapa rusuk pada kubus?", 12, [8, 10, 12, 14]),
    ]

    @staticmethod
    def generate_random_task() -> MathTask:
        question_data = random.choice(MathQuiz.QUESTIONS)
        question, answer, options = question_data
        shuffled_options = options.copy()
        random.shuffle(shuffled_options)
        return MathTask(question, answer, shuffled_options)

class GameAmongUsMath:
    def __init__(self, num_players: int = 6):
        self.players: List[Player] = []
        self.num_players = num_players
        self.num_impostors = max(1, num_players // 4)
        self.state = GameState.LOBBY
        self.current_round = 0
        self.total_tasks_needed = 25
        self.tasks_completed = 0

    def create_players(self, names: List[str] = None):
        """Buat pemain dengan nama custom atau default"""
        if names is None:
            names = [f"Player {i+1}" for i in range(self.num_players)]
        
        for i, name in enumerate(names[:self.num_players]):
            self.players.append(Player(name, i+1))

    def assign_roles(self):
        """Tentukan impostor secara random"""
        impostors = random.sample(self.players, self.num_impostors)
        for impostor in impostors:
            impostor.is_impostor = True

    def display_game_intro(self):
        """Tampilkan intro game"""
        print("\n" + "="*60)
        print("  🚀 AMONG US: MATH EDITION 🚀".center(60))
        print("="*60)
        print("\nSelamat datang di game Among Us dengan soal matematika!")
        print("Crewmate harus menyelesaikan task matematika.")
        print("Impostor harus mengganggu dan menyabotase!")
        print("\n" + "="*60 + "\n")

    def display_players_info(self):
        """Tampilkan informasi pemain"""
        print("\n👥 INFORMASI PEMAIN:")
        print("-" * 60)
        for player in self.players:
            role = "👿 IMPOSTOR" if player.is_impostor else "👨 CREWMATE"
            status = "✅ ALIVE" if player.is_alive else "💀 DEAD"
            print(f"{player.name:20} | {role:15} | {status}")
        print("-" * 60 + "\n")

    def start_game(self):
        """Mulai permainan"""
        self.state = GameState.TASK_PHASE
        self.current_round = 1
        print("\n🎮 PERMAINAN DIMULAI!\n")

    def task_phase(self):
        """Fase di mana crewmate mengerjakan task"""
        print(f"\n{'='*60}")
        print(f"ROUND {self.current_round} - FASE TASK".center(60))
        print(f"{'='*60}\n")

        alive_crewmates = [p for p in self.players if p.is_alive and not p.is_impostor]
        
        if not alive_crewmates:
            self.state = GameState.IMPOSTOR_WIN
            return

        for crewmate in alive_crewmates:
            print(f"\n🧑 Giliran {crewmate.name}...")
            time.sleep(1)

            # Generate task
            task = MathQuiz.generate_random_task()
            
            print(f"\n❓ SOAL MATEMATIKA:")
            print(f"{task.question}\n")
            print("Pilihan jawaban:")
            for i, option in enumerate(task.options, 1):
                print(f"  {i}. {option}")

            # Input jawaban
            while True:
                try:
                    choice = int(input("\nPilih jawaban (1-4): "))
                    if 1 <= choice <= 4:
                        break
                    print("❌ Input tidak valid. Pilih 1-4!")
                except ValueError:
                    print("❌ Masukkan angka yang valid!")

            answer = task.options[choice - 1]

            if task.check_answer(answer):
                print(f"✅ BENAR! {crewmate.name} berhasil menyelesaikan task!")
                crewmate.tasks_completed += 1
                self.tasks_completed += 1
            else:
                print(f"❌ SALAH! Jawaban yang benar adalah {task.correct_answer}")

            time.sleep(1)

    def voting_phase(self):
        """Fase di mana pemain voting untuk mengeluarkan pemain"""
        print(f"\n{'='*60}")
        print("🗳️  FASE VOTING".center(60))
        print(f"{'='*60}\n")

        print("Ada sosial pertemuan! Siapa yang mencurigakan?\n")

        alive_players = [p for p in self.players if p.is_alive]

        if len(alive_players) < 2:
            return

        # Display candidates
        print("Pemain yang bisa di-voting out:")
        for i, player in enumerate(alive_players, 1):
            print(f"  {i}. {player.name}")

        while True:
            try:
                choice = int(input("\nVote siapa? (masukkan nomor): "))
                if 1 <= choice <= len(alive_players):
                    break
                print("❌ Input tidak valid!")
            except ValueError:
                print("❌ Masukkan angka yang valid!")

        voted_out = alive_players[choice - 1]
        voted_out.is_alive = False

        if voted_out.is_impostor:
            print(f"\n✅ {voted_out.name} adalah IMPOSTOR!")
            print("🎉 CREWMATE MENANG!")
            self.state = GameState.CREW_WIN
        else:
            print(f"\n💀 {voted_out.name} adalah CREWMATE!")
            print("😈 IMPOSTOR TERTAWA...")

    def check_win_conditions(self):
        """Cek kondisi kemenangan"""
        alive_crewmates = [p for p in self.players if p.is_alive and not p.is_impostor]
        alive_impostors = [p for p in self.players if p.is_alive and p.is_impostor]

        # Jika semua task selesai
        if self.tasks_completed >= self.total_tasks_needed:
            self.state = GameState.CREW_WIN
            return

        # Jika impostor lebih banyak atau sama dengan crewmate
        if len(alive_impostors) >= len(alive_crewmates):
            self.state = GameState.IMPOSTOR_WIN
            return

        # Jika tidak ada crewmate yang hidup
        if len(alive_crewmates) == 0:
            self.state = GameState.IMPOSTOR_WIN
            return

    def display_results(self):
        """Tampilkan hasil akhir game"""
        print("\n" + "="*60)
        print("🏁 HASIL AKHIR GAME 🏁".center(60))
        print("="*60 + "\n")

        if self.state == GameState.CREW_WIN:
            print("🎉 CREWMATE MENANG! 🎉\n")
            print("Tim crewmate berhasil menyelesaikan semua task!")
        else:
            print("😈 IMPOSTOR MENANG! 😈\n")
            print("Impostor berhasil bertahan!")

        print("\n📊 STATISTIK AKHIR:")
        print("-" * 60)
        for player in self.players:
            role = "IMPOSTOR" if player.is_impostor else "CREWMATE"
            status = "ALIVE" if player.is_alive else "DEAD"
            print(f"{player.name:20} | {role:10} | {status:10} | Task: {player.tasks_completed}")
        print("-" * 60)

        print(f"\nTotal task diselesaikan: {self.tasks_completed}/{self.total_tasks_needed}")

    def play(self):
        """Jalankan game lengkap"""
        self.display_game_intro()

        # Setup
        print("Membuat pemain...")
        player_names = []
        for i in range(self.num_players):
            name = input(f"Masukkan nama pemain {i+1}: ").strip()
            if not name:
                name = f"Player {i+1}"
            player_names.append(name)

        self.create_players(player_names)
        self.assign_roles()
        self.display_players_info()

        input("Tekan ENTER untuk memulai game...")

        # Game loop
        self.start_game()

        while self.state == GameState.TASK_PHASE:
            self.task_phase()
            self.voting_phase()
            self.check_win_conditions()

            if self.state != GameState.GAME_OVER:
                self.current_round += 1
                print("\n" + "="*60)
                print(f"Round {self.current_round} dimulai...".center(60))
                print("="*60)
                input("Tekan ENTER untuk melanjutkan...")

        # End game
        self.display_results()

def main():
    """Fungsi utama"""
    print("\n🎮 KONFIGURASI GAME 🎮\n")
    
    while True:
        try:
            num_players = int(input("Berapa jumlah pemain? (3-15): "))
            if 3 <= num_players <= 15:
                break
            print("❌ Jumlah pemain harus antara 3-15!")
        except ValueError:
            print("❌ Masukkan angka yang valid!")

    game = GameAmongUsMath(num_players)
    game.play()

    # Tanya main lagi
    while True:
        play_again = input("\nMain lagi? (y/n): ").lower()
        if play_again == 'y':
            main()
        elif play_again == 'n':
            print("\nTerima kasih telah bermain! 👋")
            break
        else:
            print("❌ Input tidak valid! Pilih y atau n!")

if __name__ == "__main__":
    main()

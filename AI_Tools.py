import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog  # 顯示對話
import matplotlib.pyplot as plt
import pygame
import pyaudio
import wave
import keyboard

from Speech_Emotion.e_Good.wav2vec2_lg_xlsr_en_speech_emotion_recognition import Test

def TKWin():
    global win
    win=tk.Tk()
    win.geometry("400x600")    # 設定主視窗大小
    win.title("AI Tools")
    win.option_add("*Font", "王漢宗特黑體繁 26")
    win.option_add("*background",  "lightblue")
    win.configure(bg="lightblue")
    Center_Screen(win, 400, 600)

    frame1 = tk.Frame(win)
    frame1.pack()

    bt_FaceEmo = tk.Button(frame1, text='表情情緒辨識', command=FaceEmo,bg='white')
    bt_FaceEmo.grid(row=0, column=0,padx=30,pady=30,columnspan=2)
    global win_VEO_Opened
    win_VEO_Opened = False
    bt_VoiceEmo = tk.Button(frame1, text='語音情緒辨識', command=VE_Option,bg='white')
    bt_VoiceEmo.grid(row=1, column=0,padx=30,pady=30,columnspan=2)
    global win_TEO_Opened
    win_TEO_Opened = False
    bt_TextEmo = tk.Button(frame1, text='文字情緒辨識', command=TE_Option,bg='white')
    bt_TextEmo.grid(row=2, column=0,padx=30,pady=30,columnspan=2)

    win.mainloop()    # This function enters the Tkinter event loop, where the application will wait for events (such as button clicks or keypresses) and respond to them.

# 從螢幕中央開啟
def Center_Screen(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_coordinate = (screen_width - width) // 2
    y_coordinate = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")

# 從母視窗中央開啟
def Center_window(parent, window, width, height):
    # Get the coordinates of the parent window
    parent_geometry = parent.geometry()
    parent_x, parent_y = map(int, parent_geometry.split('+')[1:])
    # Calculate the center coordinates for the new window
    center_x = parent_x + (parent.winfo_width()-width)//2
    center_y = parent_y + (parent.winfo_height()-height)//2
    window.geometry(f"{width}x{height}+{center_x}+{center_y}")

# Button functions
def FaceEmo():
    from FacialExpression_Emotion._Deepface import Deepface_Test
    print("開啟即時臉部情緒辨識")

def VE_Option():
    global win_VEOption
    global win_VEO_Opened
    global win_Recording_Opened
    if win_VEO_Opened == False:
        win_VEOption = tk.Toplevel(win)
        win_VEOption.title("聲音情緒辨識")
        win_VEOption.geometry("1000x200")
        Center_window(win, win_VEOption, 1000, 200)
        win_VEOption.attributes("-topmost", True)
        win_VEO_Opened = True
        win_Recording_Opened = False

        frame1 = tk.Frame(win_VEOption)
        frame1.pack(anchor="nw", padx=10)

        global label_Path
        global file_Path
        global label_Result
        file_Path = ""
        label_Path = tk.Label(frame1, text="音檔路徑為：", font=("王漢宗特黑體繁", 8))
        label_Path.grid(row=0, column=0,padx=0, pady=20, sticky="w")
        label_Result = tk.Label(frame1, text="", font=("王漢宗特黑體繁", 8))
        label_Result.grid(row=1, column=0, padx=0, pady=20, sticky="w")

        frame2 = tk.Frame(win_VEOption)
        frame2.pack()

        bt_ChangeAudio = tk.Button(frame2, text='更換路徑音檔', command=ChangeAudio,bg='white')
        bt_ChangeAudio.grid(row=1, column=0,padx=30,pady=0)
        bt_RecordAudio = tk.Button(frame2, text='錄製音檔', command=RecordAudio,bg='white')
        bt_RecordAudio.grid(row=1, column=1,padx=30,pady=0)
        bt_PlayAudio = tk.Button(frame2, text='Play', command=PlayAudio,bg='white')
        bt_PlayAudio.grid(row=1, column=2,padx=30,pady=0)
        bt_VoiceAnalysis = tk.Button(frame2, text='分析音檔', command=VoiceEmo,bg='white')
        bt_VoiceAnalysis.grid(row=1, column=3,padx=30,pady=0)

        win_VEOption.protocol("WM_DELETE_WINDOW", WindowClose_VEO)

def WindowClose_VEO():
    global win_VEO_Opened
    win_VEO_Opened = False
    win_VEOption.destroy()

def ChangeAudio():
    global file_Path
    win.attributes("-topmost", True)
    file_Path = filedialog.askopenfilename()
    win.attributes("-topmost", False)
    label_Path.config(text= "音檔路徑為：" + file_Path)
    label_Result.config(text="")

def PlayAudio():
    global file_Path
    if not file_Path == "":
        pygame.mixer.init()
        pygame.mixer.music.load(file_Path)
        pygame.mixer.music.play()
    else:
        win.attributes("-topmost", True)
        messagebox.showwarning("Warning", "請點擊「更換路徑音檔」以取得音檔")
        win.attributes("-topmost", False)

def RecordAudio():
    global folder_path
    global win_Recording
    global win_Recording_Opened
    if not win_Recording_Opened:
        win.attributes("-topmost", True)
        folder_path = filedialog.askdirectory()
        win.attributes("-topmost", False)

        win_Recording = tk.Toplevel(win_VEOption)
        win_Recording.title("錄製音檔")
        win_Recording.geometry("800x200")
        Center_window(win_VEOption, win_Recording, 800, 200)
        win_Recording.attributes("-topmost", True)
        win_Recording_Opened = True

        frame1 = tk.Frame(win_Recording)
        frame1.pack(anchor="nw", padx=10)

        label_AudioDir = tk.Label(frame1, text="儲存資料夾路徑："+folder_path, font=("王漢宗特黑體繁", 8))
        label_AudioDir.grid(row=0, column=0,padx=0, pady=20, sticky="w")

        frame2 = tk.Frame(win_Recording)
        frame2.pack()

        bt_RecordAudio = tk.Button(frame2, text='錄製音檔', command=Record,bg='white')
        bt_RecordAudio.grid(row=1, column=0,padx=30,pady=0)

        win_Recording.protocol("WM_DELETE_WINDOW", WindowClose_RA)

def Record():
    global folder_path
    output_file = folder_path + "/recorded_audio.wav"
    duration = 5

    audio = pyaudio.PyAudio()  # 初始化 PyAudio 物件
    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=44100,
                        input=True,
                        frames_per_buffer=1024)

    print("Recording...")
    frames = []

    for i in range(0, int(44100 / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)

    print("Finished recording.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open(output_file, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(frames))

    print("Audio saved to", output_file)

def WindowClose_RA():
    global win_Recording_Opened
    win_Recording_Opened = False
    win_Recording.destroy()

def VoiceEmo():
    if file_Path != "":
        label_Result.config(text="正在進行語音情緒辨識...")
        print("開啟語音情緒辨識")
        result = Test.Result(file_Path)
        # max_emotion = max(result, key=result.get)
        label_Result.config(text="測試結果為：" + str(result))
        print(result)

        # 長條圖
        labels = list(result.keys())
        values = list(result.values())
        plt.figure(figsize=(10, 6))
        plt.bar(labels, values, color='skyblue')
        plt.title('Emotion Scores')
        plt.xlabel('Emotion')
        plt.ylabel('Score')
        win_VEOption.attributes("-topmost", False)
        plt.show()

    else:
        win.attributes("-topmost", True)
        messagebox.showwarning("Warning", "請點擊「更換路徑音檔」以取得音檔")
        win.attributes("-topmost", False)

def TE_Option():
    global win_TEOption
    global win_TEO_Opened
    if not win_TEO_Opened:
        win_TEOption = tk.Toplevel(win)
        win_TEOption.title("文字情緒辨識")
        win_TEOption.geometry("1000x200")
        Center_window(win, win_TEOption, 1000, 200)
        win_TEOption.attributes("-topmost", True)
        win_TEO_Opened = True

        frame1 = tk.Frame(win_TEOption)
        frame1.pack(anchor="nw", padx=10)

def main():
    TKWin()

main()
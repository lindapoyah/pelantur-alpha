import tkinter as tk
from tkinter import filedialog, messagebox
from pydub import AudioSegment
import subprocess
import os
import glob

voice_path=""
music_path=""
image_files=[]
output_folder=""

def upload_voice():
    global voice_path
    f=filedialog.askopenfilename(filetypes=[("Audio","*.mp3 *.wav *.m4a")])
    if f:
        voice_path=f
        voice_entry.delete(0,tk.END)
        voice_entry.insert(0,f)

def upload_images():
    global image_files
    files=filedialog.askopenfilenames(filetypes=[("Images","*.jpg *.jpeg *.png")])
    if files:
        image_files=list(files)
        images_entry.delete(0,tk.END)
        images_entry.insert(0,f"{len(image_files)} images selected")

def upload_music():
    global music_path
    f=filedialog.askopenfilename(filetypes=[("Audio","*.mp3 *.wav")])
    if f:
        music_path=f
        music_entry.delete(0,tk.END)
        music_entry.insert(0,f)

def choose_output_folder():
    global output_folder
    folder=filedialog.askdirectory()
    if folder:
        output_folder=folder
        output_folder_entry.delete(0,tk.END)
        output_folder_entry.insert(0,folder)

def get_audio_duration(file):
    audio=AudioSegment.from_file(file)
    return len(audio)/1000

def cleanup_temp_files():
    try:
        for f in glob.glob("temp_*.mp4"):
            os.remove(f)

        temp_files=[
            "concat.txt",
            "images.txt",
            "slideshow.mp4",
            "audio_mix.m4a"
        ]

        for f in temp_files:
            if os.path.exists(f):
                os.remove(f)

    except:
        pass

def render_video():

    if not voice_path:
        messagebox.showerror("Error","Voice belum dipilih")
        return

    if not image_files:
        messagebox.showerror("Error","Images belum dipilih")
        return

    if not output_folder:
        messagebox.showerror("Error","Folder output belum dipilih")
        return

    name=output_name_entry.get()

    if not name:
        messagebox.showerror("Error","Nama file kosong")
        return

    try:

        voice_duration=get_audio_duration(voice_path)

        total_duration=voice_duration+3

        dur_per_img=total_duration/len(image_files)

        temp_videos=[]

        for i,img in enumerate(image_files):

            temp=f"temp_{i}.mp4"

            fade_out_start=dur_per_img-0.5

            cmd=[
            "ffmpeg","-y",
            "-loop","1",
            "-i",img,
            "-t",str(dur_per_img),
            "-vf",
            f"scale=1280:720,fps=24,"
            f"fade=t=in:st=0:d=0.5,"
            f"fade=t=out:st={fade_out_start}:d=0.5",
            "-pix_fmt","yuv420p",
            "-c:v","libx264",
            "-preset","fast",
            temp
            ]

            subprocess.run(cmd,check=True)

            temp_videos.append(temp)

        with open("concat.txt","w") as f:
            for v in temp_videos:
                f.write(f"file '{v}'\n")

        slideshow="slideshow.mp4"

        cmd_concat=[
        "ffmpeg","-y",
        "-f","concat",
        "-safe","0",
        "-i","concat.txt",
        "-c","copy",
        slideshow
        ]

        subprocess.run(cmd_concat,check=True)

        output=os.path.join(output_folder,name+".mp4")

        if music_path:

            vol=music_volume_slider.get()

            cmd_final=[
            "ffmpeg","-y",
            "-stream_loop","-1",
            "-i",music_path,
            "-i",voice_path,
            "-i",slideshow,
            "-filter_complex",
            f"[0:a]volume={vol},afade=t=out:st={voice_duration}:d=3[music];"
            "[music][1:a]amix=inputs=2:duration=first[a]",
            "-map","2:v",
            "-map","[a]",
            "-c:v","copy",
            "-c:a","aac",
            "-t",str(total_duration),
            output
            ]

        else:

            cmd_final=[
            "ffmpeg","-y",
            "-i",slideshow,
            "-i",voice_path,
            "-map","0:v",
            "-map","1:a",
            "-c:v","copy",
            "-c:a","aac",
            "-t",str(total_duration),
            output
            ]

        subprocess.run(cmd_final,check=True)

        cleanup_temp_files()

        messagebox.showinfo("Success","Video berhasil dibuat!")

    except subprocess.CalledProcessError:

        cleanup_temp_files()

        messagebox.showerror("Error","FFmpeg gagal render video")

root=tk.Tk()
root.title("Pelantur Beta - Software YTTA by mbombinx")
root.geometry("640x320")

main=tk.Frame(root)
main.pack(pady=20)

left=tk.Frame(main)
left.pack(side="left",padx=40)

tk.Label(left,text="SETTINGS",font=("Arial",14,"bold")).pack(anchor="w")

tk.Label(left,text="Upload Voice").pack(anchor="w")
vf=tk.Frame(left);vf.pack(anchor="w")
voice_entry=tk.Entry(vf,width=30);voice_entry.pack(side="left")
tk.Button(vf,text="Upload",command=upload_voice).pack(side="left")

tk.Label(left,text="Upload Images").pack(anchor="w",pady=(10,0))
imf=tk.Frame(left);imf.pack(anchor="w")
images_entry=tk.Entry(imf,width=30);images_entry.pack(side="left")
tk.Button(imf,text="Upload",command=upload_images).pack(side="left")

tk.Label(left,text="Upload Background Music").pack(anchor="w",pady=(10,0))
mf=tk.Frame(left);mf.pack(anchor="w")
music_entry=tk.Entry(mf,width=30);music_entry.pack(side="left")
tk.Button(mf,text="Upload",command=upload_music).pack(side="left")

tk.Label(left,text="Background Music Volume").pack(pady=(20,0))
music_volume_slider=tk.Scale(left,from_=0,to=2,resolution=0.1,orient="horizontal")
music_volume_slider.set(0.5)
music_volume_slider.pack()

right=tk.Frame(main)
right.pack(side="left",padx=40)

tk.Label(right,text="OUTPUT SETTINGS",font=("Arial",14,"bold")).pack(anchor="w")

tk.Label(right,text="Output File Name").pack(anchor="w")
output_name_entry=tk.Entry(right,width=40)
output_name_entry.pack()

tk.Label(right,text="Output Folder").pack(anchor="w",pady=(10,0))
ff=tk.Frame(right);ff.pack(anchor="w")
output_folder_entry=tk.Entry(ff,width=30)
output_folder_entry.pack(side="left")
tk.Button(ff,text="Browse",command=choose_output_folder).pack(side="left")

tk.Button(
right,
text="RENDER VIDEO",
font=("Arial",12,"bold"),
bg="#4CAF50",
fg="white",
padx=20,
pady=10,
command=render_video
).pack(pady=30)

root.mainloop()

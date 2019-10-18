import wx
import os
from flick import Flick

class MyFrame(wx.Frame):    
    def __init__(self):
        super().__init__(parent=None, title='Flick Movie Generator')

        panel = wx.Panel(self)

        f_sizer = wx.BoxSizer(wx.VERTICAL)

        font_cap = wx.Font(12, wx.FONTFAMILY_SCRIPT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        font_text = wx.Font(10, wx.FONTFAMILY_SCRIPT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)

        #v2 caption
        self.v2_cap = wx.StaticText(panel, -1, style = wx.ALIGN_CENTER)
        self.v2_cap.SetFont(font_cap)
        self.v2_cap.SetLabel("OVERLAY MOVIE:")

        #browse v2 movie
        self.v2_btn = wx.Button(panel, label="Please select...")
        self.v2_btn.Bind(wx.EVT_BUTTON, self.on_open_file)

        #add v2 to sizer
        f_sizer.Add(self.v2_cap, 0, wx.ALL | wx.EXPAND, 5)
        f_sizer.Add(self.v2_btn, 0, wx.ALL | wx.EXPAND, 5)
        
        #v3 caption dir
        self.v3_cap = wx.StaticText(panel, -1, style = wx.ALIGN_CENTER)
        self.v3_cap.SetFont(font_cap)
        self.v3_cap.SetLabel("OUTPUT FOLDER:")

        #browse v3 OUTPUT DIR
        self.v3_btn = wx.Button(panel, label="Please select...")
        self.v3_btn.Bind(wx.EVT_BUTTON, self.on_open_folder)

        #add v3 to sizer
        f_sizer.Add(self.v3_cap, 0, wx.ALL | wx.EXPAND, 5)
        f_sizer.Add(self.v3_btn, 0, wx.ALL | wx.EXPAND, 5)

        #v3 caption dir
        self.v1_cap = wx.StaticText(panel, -1, style = wx.ALIGN_CENTER)
        self.v1_cap.SetFont(font_cap)
        self.v1_cap.SetLabel("INPUT VIDEOS:")

        #v3 tooltip
        self.v1_tooltip = wx.ToolTip("List of videos:")

        #browse v1 movie
        self.v1_btn = wx.Button(panel, label="Please select...")
        self.v1_btn.SetToolTip(self.v1_tooltip)
        self.v1_btn.Bind(wx.EVT_BUTTON, self.on_open_files)

        #add v1 to sizer
        f_sizer.Add(self.v1_cap, 0, wx.ALL | wx.EXPAND, 5)
        f_sizer.Add(self.v1_btn, 0, wx.ALL | wx.EXPAND, 5)

        #vgen caption dir
        self.gen_cap = wx.StaticText(panel, -1, style = wx.ALIGN_CENTER)
        self.gen_cap.SetFont(font_cap)
        self.gen_cap.SetLabel("Generate videos:")

        #gen btn
        self.gen_btn = wx.Button(panel, label="Generate!")
        self.gen_btn.Bind(wx.EVT_BUTTON, self.generate_videos)

        #add gen to sizer
        f_sizer.Add(self.gen_cap, 0, wx.ALL | wx.EXPAND, 5)
        f_sizer.Add(self.gen_btn, 0, wx.ALL | wx.EXPAND, 5)

        self.msg = wx.MessageDialog(panel, 
                               "Please select all information before generating.",
                               "All information needed.",
                               wx.OK | wx.ICON_INFORMATION
                               )

        self.msg_ne = wx.MessageDialog(panel, 
                               "File(s)/Folder do not exist. Please reselect information.",
                               "All information needed.",
                               wx.OK | wx.ICON_WARNING
                               )

        self.msg_done = wx.MessageDialog(panel, 
                        "Video was generated succesfully.",
                        "Status",
                        wx.OK | wx.ICON_INFORMATION
                        )
        
        panel.SetSizer(f_sizer)
        f_sizer.Fit(self)
        f_sizer.SetSizeHints(self)
        panel.Fit()
        self.SetClientSize(panel.GetSize()+(150,10))
        
        self.Show()

    def on_open_folder(self, event):
        title = "Please select the folder for the final videos to be saved"
        dlg = wx.DirDialog(self, title, style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.v3_path = dlg.GetPath()
            self.v3_btn.SetLabel(dlg.GetPath())
        dlg.Destroy()

    def on_open_file(self, event):
        title = "Please select the overlay video"
        dlg = wx.FileDialog(self, title, style=wx.FD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.v2_path = dlg.GetPath()
            self.v2_btn.SetLabel(dlg.GetFilename())
        dlg.Destroy()
    
    def on_open_files(self, event):
        title = "Please select the background videos video"
        dlg = wx.FileDialog(self, title, style=wx.FD_MULTIPLE)
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            names = dlg.GetFilenames()
            self.v1_btn.SetLabel("Selected {} file(s).".format(len(paths)))
            self.v1_tooltip.SetTip("\n".join(names))
            self.v1_paths = paths
        dlg.Destroy()

    def generate_videos(self, event):
        
        if hasattr(self, 'v2_path') and hasattr(self, 'v2_path') and hasattr(self, 'v1_paths'):
            if os.path.isfile(self.v2_path) and os.path.isdir(self.v3_path) and self._verify_paths:
                for path in self.v1_paths:
                    foo = Flick(path, self.v2_path, os.path.join(self.v3_path, os.path.basename(path)))
                    status = foo.run()
                    if status == -1:
                        self.msg_done.SetMessage("Video {} allready exists in the output folder. Please move/delete it before you can generate a new one.".format(path))
                    else:
                        self.msg_done.SetMessage("Video {} was succesfully generated.".format(os.path.basename(path)))
                    self.msg_done.ShowModal()
            else:
                self.msg_ne.ShowModal()
        else:
            self.msg.ShowModal()

    def _verify_paths(self):
        #verify if paths exists
        if len(self.v1_paths) == 0:
            return False

        for el in self.v1_paths:
            if not os.path.isfile(el):
                return False

        return True

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()
import os
import pandas as pd
import tkinter.filedialog as tkfd

d_ext_desc = {'csv':'CSV file',
              'db':'Thumbnail',
              'doc':'Microsoft Word Document',
              'docx':'Microsoft Word Document',
              'GIF':'GIF Image file',
              'html':'HTML file',
              'ico':'Icon Image file',
              'jpg':'JPG Image file',
              'JPEG':'JPEG Image file',
              'json':'JSON file',
              'lnk':'Shortcut file',
              'msg':'Microsoft Outlook Message file',
              'pdf':'PDF file',
              'pkl':'Pickle (python) file',
              'png':'PNG Image file',
              'ppt':'Microsoft Powerpoint file',
              'pptx':'Microsoft Powerpoint file',
              'pst':'Microsoft Outlook Data file',
              'py':'Python file',
              'pyc':'Python file (compiled)',
              'rtf':'Rich Text Format',
              'svg':'SVG Image file',
              'txt':'Text document',
              'url':'Hyperlink',
              'vsd':'Microsoft Visio file',
              'xls':'Microsoft Excel file',
              'xlsb':'Microsoft Excel file',
              'xlsm':'Microsoft Excel (Macro-enabled) file',
              'xlsx':'Microsoft Excel file',
              'yml':'Requirements file (python)',
              'dwg':'Auto CAD DWG file',
              'dxf':'Auto CAD DXF file',
              'bak':'Auto CAD BackUP file',
              'psd':'Photoshop',
              'skp':'Sketchup',
              'max':'3D Max file',
              'log':'Log File',
              'tmp':'Temporary File',
              'jpeg':'JPEG Image File',
              'rar':'WinRar File',
              'tif':'TIFF File',
              'kmz':'Google Earth KMZ File',
              'kml':'Googel Earth KML File',
              'zip':'ZIP file'}

def ext_desc(ext):
    try:
        desc = d_ext_desc[ext]
    except KeyError:
        desc = ''
    else:
        pass
    return desc

path = tkfd.askdirectory() # Request for path

def generate_index(path=path, max=0):
    # stops generating index whenever there are more than 500 records, to test if the script works
    # use 'max=0' to generate the full index
    
    #path = path if path else tkfd.askdirectory() # Request path if not provided

    df = pd.DataFrame(columns=['File','File Type','Folder Location','Link','Path'])
    for root, _ , files in os.walk(path):
        files = [f for f in files if not f.startswith('~') and f!='Thumbs.db']
        paths = [os.path.join(root, f) for f in files]
        exts = [os.path.splitext(f)[1][1:].lower() for f in files]
        filetypes = [ext_desc(ext) for ext in exts]
        file_links = ['=HYPERLINK("{}","link")'.format(p) if len(p) < 256 else '' for p in paths]
        folders = [os.path.dirname(p) for p in paths]
        df1 = pd.DataFrame({'File': files,
                            'File Type': filetypes,
                            'Folder Location': folders,
                            'Link': file_links,
                            'Path': paths})
        df = pd.concat([df,df1])
        if max and (df.shape[0]>max):
            break
    df = df.reset_index(drop=True)
    return df
  
if __name__ == '__main__':
    df = generate_index(max=0)
    save_location = path + "/" + "files_index.xlsx"
    df.to_excel(save_location,sheet_name="Hyperlinks",freeze_panes=[1,0])
    
#hosted with ❤ by GitHub

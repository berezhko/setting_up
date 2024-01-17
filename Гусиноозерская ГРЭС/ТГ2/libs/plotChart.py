import pandas as pd
import matplotlib.pyplot as plt
from numpy import *


# Возврящаем max и min (округляя до большего для max, и меньшего для min значения) из data если ключь присутствует в списке lst.
# return scaleforpss={"Ug": [0.97, 1.08], "Ig": [0.52, 0.68], "Uf2": [0.39, 1.51], "If": [0.55, 0.94], "Pg": [0.58, 0.64], "Qg": [-0.23, 1.07]}
# Данная строка исппользуется в print_oscilogram для создания изображения фиксированного значения
def scaleForPSS(data, lst=["Ug", "Ig", "Uf2", "If", "Pg", "Qg"]):
    print("scaleforpss={", end='')
    size_lst = size(lst)
    num_round = 2
    delta = 10**(-num_round)
    end=', '
    for i, k in enumerate(lst):
        if k in data.keys():
            if size_lst == i+1:
                end = '}'
            print("\"{0}\": [{1}, {2}]".format(k, round(min(data[k])-delta, num_round), round(max(data[k])+delta, num_round)),end=end)

def scaleForPSS2(data1, data2, lst=["Ug", "Ig", "Uf2", "If", "Pg", "Qg"]):
    print("scaleforpss={", end='')
    size_lst = size(lst)
    num_round = 2
    delta = 10**(-num_round)
    end=', '
    for i, k in enumerate(lst):
        if k in data1.keys() and k in data2.keys():
            if size_lst == i+1:
                end = '}\n'
            print("\"{0}\": [{1}, {2}]".format(k, round( min(min(data1[k]), min(data2[k])) - delta, num_round), round( max(max(data1[k]), max(data2[k])) + delta, num_round)),end=end)

# Вычисляет начало и конец опытов толчка используя производные массива arr
def getIntervalRamp(arr, num_std=10, time_before=5, time_after=15):
    d = arr.diff()
    mask = (d < d.mean() - num_std*d.std()) | (d.mean() + num_std*d.std() < d)
    for idx in range(size(d[mask])):
        last_index = min(arr.index[-1], d[mask].index[idx] + time_after*100)
        first_index = max(arr.index[0], d[mask].index[idx] - time_before*100)
        if d[mask][d[mask].index[idx]] >= 0:
            print("up\t", end="")
        else:
            print("down\t", end="")
        print("be=({}, {})".format(round(first_index/100, 2), round(last_index/100, 2)))

def findMinPoint(df):
    for i in df[df == min(df)].index:
        print("index_min = {}".format(i))


def findMaxPoint(df):
    for i in df[df == max(df)].index:
        print("index_max = {}".format(i))


def printDebug(df):
    for i in df.keys():
        print(i, end=", ")
    print()

    if 'Uf2' in df.keys():
        print("Uf2:", end="\t")
        findMinPoint(df['Uf2'])
        print("    ", end="\t")
        findMaxPoint(df['Uf2'])
    elif 'Alpha gr' in df.keys():
        print("Alpha gr", end="\t")
        findMinPoint(df['Alpha gr'])
        print("        ", end="\t")
        findMaxPoint(df['Alpha gr'])


#Печать результата
def myplot(x, y, nominal, axs, legnd, header="", color="black", scale="Задается при вызове myplot в print_oscilogram", scaleforpss=[0, 0], second_plot=False, prev_twinx_axes="None"):
    result = prev_twinx_axes
    
    axs.plot(x, nominal*y, linewidth=3, label=legnd.split(",")[0], color=color)
    axs.set_xlim(min(x), max(x))
    
    ymax = max(nominal*y)
    ymin = min(nominal*y)
    if second_plot:
        y1, y2 = axs.get_ylim()
        previous_ymax = (y2 + scale*(y1 + y2)) / (1 + 2*scale)
        previous_ymin = (y1 + scale*(y1 + y2)) / (1 + 2*scale)
        ymax = max(ymax, previous_ymax)
        ymin = min(ymin, previous_ymin)
    ds = (ymax - ymin)*scale
    axs.set_ylim(ymin - ds, ymax + ds)
        
    if scaleforpss[0] != scaleforpss[1]:
        ymax = nominal*scaleforpss[1]
        ymin = nominal*scaleforpss[0]
        axs.set_ylim(ymin, ymax)
        
    if nominal != 1:
        if second_plot and prev_twinx_axes != "None":
            axes_right = prev_twinx_axes
        else:
            axes_right = axs.twinx()
        y1, y2 = axs.get_ylim()
        ymax = (y2 + scale*(y1 + y2)) / (1 + 2*scale)
        ymin = (y1 + scale*(y1 + y2)) / (1 + 2*scale)
        ds = (ymax - ymin)*scale
        axes_right.set_ylim((ymin-ds)/nominal, (ymax+ds)/nominal)
        axes_right.set_ylabel("[pu]")
        
        result = axes_right

    if second_plot == False:
        axs.set_ylabel(legnd)
    if header != "":
        axs.set_title(header, loc="left", fontsize=28, fontname="serif", color="blue", pad=20)
    axs.legend(loc="best")
    axs.minorticks_on()
    axs.grid(which="major", color="b", alpha=0.4, linestyle="dashed", linewidth=1.0)
    axs.grid(which="minor", color="b", alpha=0.4, linestyle="dashed", linewidth=0.5, axis="both")
        
    return result

        
def gen(arr, filtr):
    class Filter():
        def __init__(self, size_data=10):
            self.data = []
            self.size_data = size_data
        def add(self, value):
            self.data.append(value)
            if size(self.data) > self.size_data:
                self.data = self.data[1:]
            return mean(self.data)

    f = Filter(filtr)
    return array([f.add(i) for i in arr])


def mysavefig(img_name, bbox_inches='tight', pad_inches=0):
    plt.savefig(img_name[:-4]+".png", bbox_inches=bbox_inches, pad_inches=pad_inches)


def replase_number_delim_in_file(file_name):
    with open(file_name) as f:
        lines = f.readlines()
        newlines = [l.replace(',', '.') for l in lines]
    with open(file_name, "w") as f:
        f.writelines(newlines)


def print_oscilogram(file_name, be=(0, -1), calc=[], set_color="C0", not_plot=[], filters={}, def_filters=1, add_chart=[], scale={}, def_scale=0.02, img_name="", debug=False, scaleforpss={}):
    scale_copy = scale.copy()
    filters_copy = filters.copy()
    scaleforpss_copy = scaleforpss.copy()
    
    replase_number_delim_in_file(file_name)
    df = pd.read_csv(file_name, sep=';', skiprows=1)
    with open(file_name) as f:
        head_line = f.readline()
        start_time = head_line.split(";")[0].split(" ")[2]+" "+head_line.split(";")[0].split(" ")[-1]
    title = "Начало опыта: {0}".format(start_time)
    
    begin = int(be[0]*100)
    if be[1] != -1:
        end = int(be[1]*100)
    else:
        end = -1
    df = df[begin:end]
    
    cos_nom = 0.85
    te_u2_nom = 835
    ud_nom = 420
    if_nom = 1890
    ug_nom = 15750
    ig_nom = 9490
    pg_nom = 220
    qg_nom = 135
    Xa = 0.0222
    Ra = 0.0005

    if "Alpha gr" not in df.keys() and "AlphaAvr" in df.keys():
            df["Alpha gr"] = df["AlphaAvr"]

    if "ig" in calc and all([key in df.keys() for key in ["Ug", "Pg", "Qg"]]):
        df["Ig2"] = pd.Series(1e6*pg_nom * df.Pg * sqrt(1 + (tan(arccos(cos_nom))*df.Qg/df.Pg)**2) / (df.Ug*ug_nom*sqrt(3))/ ig_nom)
        
    if "uf" in calc and all([key in df.keys() for key in ["Alpha gr", "If", "Ug"]]) and all(df.Ug > 0.01):
        komutatsia = arccos(cos(pi*df['Alpha gr']/180) - sqrt(2)*Xa*df.If*if_nom/(te_u2_nom*df.Ug) ) - pi*df['Alpha gr']/180
        df['Uf2'] = pd.Series( (te_u2_nom*3*sqrt(2)/pi*df.Ug*cos(pi*df['Alpha gr']/180) - 3*Xa/pi*df.If*if_nom  - (2 - 3*komutatsia/(2*pi))*Ra*df.If*if_nom  - 2*2)/ud_nom )
        
    if "iq" in calc and all([key in df.keys() for key in ["Ug", "Qg"]]):
        df["Iq2"] = pd.Series(1e6*qg_nom*df.Qg / (ug_nom*df.Ug * sqrt(3)) / ig_nom)
        
    if "ip" in calc and all([key in df.keys() for key in ["Ug", "Pg"]]):
        df["Ip2"] = pd.Series(1e6*pg_nom*df.Pg / (ug_nom*df.Ug * sqrt(3)) / ig_nom)

    if debug == True:
        printDebug(df)

    not_plot.append("time")
    plot_data = {}
    for key in list(df):
        if key in not_plot:
            continue
        plot_data[key] = df[key]
    
    nominals = {"Ug": ug_nom, "Ig": ig_nom, "Uf": ud_nom, "Ig2": ig_nom, "Uf2": ud_nom, "If": if_nom, "Pg": pg_nom, "Qg": qg_nom, "Iq2": ig_nom, "Ip2": ig_nom}
    legends = {"Ug": "Ug, [B]", "Ig": "Ig, [A]", "Uf": "Uf, [B]", "Ig2": "Ig, [A]", "Uf2": "Uf, [B]", "If": "If, [A]", "Pg": "Pg, [МВат]", "Qg": "Qg, [МВар]", "Iq2": "Iq, [A]", "Ip2": "Ip, [A]"}
    
    fig, axs = plt.subplots(len(plot_data), 1)

    for i, pl in enumerate(plot_data):
        if pl not in nominals.keys():
            nominals[pl] = 1
            
        if pl not in legends.keys():
            legends[pl] = pl + ", [pu]"
            
        if pl not in filters_copy.keys():
            filters_copy[pl] = def_filters

        if pl not in scale_copy.keys():
            scale_copy[pl] = def_scale
            
        if pl not in scaleforpss_copy.keys():
            scaleforpss_copy[pl] = [0, 0]
            
        if set_color == "rainbow":
            color="C{}".format(i)
        else:
            color=set_color
        
        twinx_axes = myplot(df.time, gen(plot_data[pl], filters_copy[pl]), nominals[pl], axs[i],  legnd=legends[pl],
                                 header=title, color=color, scale=scale_copy[pl], scaleforpss=scaleforpss_copy[pl])
        
        if "ousyn" in add_chart and pl == "Usyn" and "SetLimUsynAct" in df.keys():
            myplot(df.time, df["SetLimUsynAct"], 1, axs[i],  legnd="SetLimUsynAct", 
                   header=title, color="red", scale=scale_copy[pl], second_plot=True, prev_twinx_axes=twinx_axes)
        
        elif "omv" in add_chart and pl == "Qg" and "SetLimQg" in df.keys():
            myplot(df.time, df["SetLimQg"], nominals["Qg"], axs[i],  legnd="SetLimQg", 
                   header=title, color="red", scale=scale_copy[pl], second_plot=True, prev_twinx_axes=twinx_axes)
        
        elif "vhz" in add_chart and pl == "Ug" and "MaxSetUgV/Hz" in df.keys():
            myplot(df.time, df["MaxSetUgV/Hz"], nominals["Ug"], axs[i],  legnd="MaxSetUgV/Hz", 
                   header=title, color="red", scale=scale_copy[pl], second_plot=True, prev_twinx_axes=twinx_axes)

        title = ""
    
    if img_name == "":
        img_name = file_name
    mysavefig(img_name, bbox_inches='tight', pad_inches=0)

    return df

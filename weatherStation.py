import os
import csv

def getCloudStatus():
        Wfile = "C:\\Users\\Win10\\Documents\\Weather\\CloudWatcher.csv"        
        if Wfile and os.path.exists(Wfile):
            with open(Wfile, "r", encoding="utf-8", errors="ignore") as scraped:
                lines = scraped.read().splitlines()
                last_line = lines[-2]
                clouds = last_line.split(",")[2]
            return (clouds)
        else:
            return ("noInfo")
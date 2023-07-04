import subprocess
import time
import kalibrate

seconds = 30
frequencies = []

def extract_base_frequencies(data):
    base_frequencies = []
    for entry in data:
        if 'base_freq' in entry:
            base_frequencies.append(entry['base_freq'])
    return base_frequencies

def ScanFreq():
    global frequencies
    print("Scanning for towers this takes a minute")
    scanner = kalibrate.Kal("/home/dellpc/kalibrate-bladeRF/src/kal")
    # Scan a band
    band_results = scanner.scan_band("GSM900", gain=60)
    
    frequencies = extract_base_frequencies(band_results)#file.read().splitlines()
    print("Found towers: " + str(len(frequencies)))
def ScanDevices():
    global frequencies
    # Check if there is more than one frequency
    if len(frequencies) > 1:
        # Iterate over the frequencies and run grgsm_livemon
        for frequency in frequencies:
            frequency = str(frequency).replace(".0", "").replace(",0", "")
            print(f"Running grgsm_livemon -f {frequency}")
            try:
                subprocess.run(["grgsm_livemon", "-f", frequency ,"-g 60"],timeout=seconds)
            except:
                s = ""
            #time.sleep(120)  # Sleep for 2 minutes
    elif len(frequencies) == 1:
        print("Only one frequency found. Skipping rotation.")
        frequency = frequencies[0]
        frequency = str(frequency).replace(".0", "").replace(",0", "")
        print(f"Running grgsm_livemon -f {frequency}")
        try:
            subprocess.run(["grgsm_livemon", "-f", frequency,"-g 60"])
        except:
            s=""

print("####Scanner started####")
while 1:
    if len(frequencies) == 0:
        ScanFreq()
    ScanDevices()
    print("#### Reset #####")

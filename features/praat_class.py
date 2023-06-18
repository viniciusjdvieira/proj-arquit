from scipy.io import wavfile
import numpy as np
from scipy.io.wavfile import read
import numpy as np
from audio_format import pcm2float
import parselmouth
from parselmouth.praat import call

class Sinal:
    def __init__(self, filename):
        self.filename = filename

    def carrega(self):
        self.rate, self.signal = wavfile.read(self.filename)
        # sndG é o sinal convertido para float32
        self.sndG = pcm2float(self.signal)
        # sndPraat é o float32 no formato da biblioteca do Praat
        self.sndPraat = parselmouth.Sound(self.sndG)

    def pitch(self):
        self.pitchPraat = call(self.sndPraat, "To Pitch", 0.0, 75, 600)
        self.meanF0 = call(self.pitchPraat, "Get mean", 0, 0, "Hertz")  # get mean pitch
        self.stdevF0 = call(self.pitchPraat, "Get standard deviation", 0, 0, "Hertz")  # get standard deviation
        self.minF0 = call(self.pitchPraat, "Get minimum", 0.0, 0.0, "Hertz", "Parabolic")   # get minimum
        self.maxF0 = call(self.pitchPraat, "Get maximum", 0.0, 0.0, "Hertz", "Parabolic")   # get maximum
        self.rangeF0 = self.maxF0 - self.minF0    # get the range of F0

    def jitter(self,jitterType="local"):
        self.jitterType=jitterType
        self.f0min = 75
        self.f0max = 600
        self.pointProcess = call(self.sndPraat, "To PointProcess (periodic, cc)", self.f0min, self.f0max)
        if self.jitterType == "local":
            self.localJitter = call(self.pointProcess, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
            self.jitt = self.localJitter * 100
        elif self.jitterType == "localabsolute":
            self.localabsoluteJitter = call(self.pointProcess, "Get jitter (local, absolute)", 0, 0, 0.0001, 0.02, 1.3)
            self.jitt = self.localabsoluteJitter
        elif self.jitterType == "rap":
            self.rapJitter = call(self.pointProcess, "Get jitter (rap)", 0, 0, 0.0001, 0.02, 1.3)
            self.jitt = self.rapJitter
        elif self.jitterType == "ppq5":
            self.ppq5Jitter = call(self.pointProcess, "Get jitter (ppq5)", 0, 0, 0.0001, 0.02, 1.3)
            self.jitt = self.ppq5Jitter
        elif self.jitterType == "ddp":
            self.ddpJitter = call(self.pointProcess, "Get jitter (ddp)", 0, 0, 0.0001, 0.02, 1.3)
            self.jitt = self.ddpJitter

    def shimmer(self, shimmerType="local"):
        self.shimmerType = shimmerType
        self.f0min = 75
        self.f0max = 600
        self.pointProcess = call(self.sndPraat, "To PointProcess (periodic, cc)", self.f0min, self.f0max)
        if self.shimmerType == "local":
            self.localShimmer = call([self.sndPraat, self.pointProcess], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
            self.shimm = self.localShimmer * 100
        elif self.shimmerType == "localdb":
            self.localdbShimmer = call([self.sndPraat, self.pointProcess], "Get shimmer (local_dB)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
            self.shimm = self.localdbShimmer
        elif self.shimmerType == "apq3":
            self.apq3Shimmer = call([self.sndPraat, self.pointProcess], "Get shimmer (apq3)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
            self.shimm = self.apq3Shimmer
        elif self.shimmerType == "apq5":
            self.aqpq5Shimmer = call([self.sndPraat, self.pointProcess], "Get shimmer (apq5)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
            self.shimm = self.aqpq5Shimmer
        elif self.shimmerType == "apq11":
            self.apq11Shimmer = call([self.sndPraat, self.pointProcess], "Get shimmer (apq11)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
            self.shimm = self.apq11Shimmer
        elif self.shimmerType == "dda":
            self.ddaShimmer = call([self.sndPraat, self.pointProcess], "Get shimmer (dda)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
            self.shimm = self.ddaShimmer

    def getHNR(self):
        self.harmonicity = call(self.sndPraat, "To Harmonicity (cc)", 0.01, 75, 0.1, 1.0)
        self.hnr = call(self.harmonicity, "Get mean", 0, 0)

    def getGNE(self,gneFreq=1000,gneType="maximum"):
        self.gneFreq=gneFreq
        self.gneType=gneType
        self.gne_praat = call(self.sndPraat, "To Harmonicity (gne)", 500, 4500, self.gneFreq, 80)
        if self.gneType == "mean":
            self.gne = call(self.gne_praat, "Get mean", 0.0, 0.0, 0.0, 0.0)
        elif self.gneType == "maximum":
            self.gne = call(self.gne_praat, "Get maximum")

    def getIntensity(self):
        self.inten = call(self.sndPraat, "To Intensity", 100, 0)
        self.meanIntensity = call(self.inten, "Get mean...", 0.0, 0.0, 'dB')
        self.stdevIntensity = call(self.inten, "Get standard deviation", 0.0, 0.0)  # get standard deviation
        self.minIntensity = call(self.inten, "Get minimum", 0.0, 0.0, "Parabolic")
        self.maxIntensity = call(self.inten, "Get maximum", 0.0, 0.0, "Parabolic")
        self.rangeIntensity = self.maxIntensity - self.minIntensity

    def getFormants(self):
        self.forman = call(self.sndPraat, "To Formant (burg)", 0.0, 5.0, 5500.0, 0.025, 50.0)
        self.meanF1 = call(self.forman, "Get mean", 1, 0.0, 0.0, 'hertz')
        self.stdevF1 = call(self.forman, "Get standard deviation", 1, 0.0, 0.0, 'hertz')
        self.maxF1 = call(self.forman, "Get maximum", 1, 0.0, 0.0, 'hertz','Parabolic')
        self.minF1 = call(self.forman, "Get minimum", 1, 0.0, 0.0, 'hertz', 'Parabolic')
        self.rangeF1 = self.maxF1 - self.minF1
        self.meanF2 = call(self.forman, "Get mean", 2, 0.0, 0.0, 'hertz')
        self.stdevF2 = call(self.forman, "Get standard deviation", 2, 0.0, 0.0, 'hertz')
        self.maxF2 = call(self.forman, "Get maximum", 2, 0.0, 0.0, 'hertz', 'Parabolic')
        self.minF2 = call(self.forman, "Get minimum", 2, 0.0, 0.0, 'hertz', 'Parabolic')
        self.rangeF2 = self.maxF2 - self.minF2
        self.meanF3 = call(self.forman, "Get mean", 3, 0.0, 0.0, 'hertz')
        self.stdevF3 = call(self.forman, "Get standard deviation", 3, 0.0, 0.0, 'hertz')
        self.maxF3 = call(self.forman, "Get maximum", 3, 0.0, 0.0, 'hertz', 'Parabolic')
        self.minF3 = call(self.forman, "Get minimum", 3, 0.0, 0.0, 'hertz', 'Parabolic')
        self.rangeF3 = self.maxF3 - self.minF3

    def getCPPS(self, time_step = 0.002):
        self.medCPPS = call(self.sndPraat, "To PowerCepstrogram", 60.0, time_step, 5000.0, 50)
        self.cpps = call(self.medCPPS, "Get CPPS", 0, 0.01, 0.001, 60.0, 330.0, 0.05, "Parabolic", 0.001, 0.0, "Straight",
                    "Robust")

    def getSlope(self):
        self.decl = call(self.sndPraat, "To Ltas", 100)    # declínio espectral
        self.slope = call(self.decl, "Get slope", 0, 1250, 1250, 4000, "dB")

import warnings


class Measurement:
    def __init__(self, type_of_measurement):
        self.type_of_measurement = type_of_measurement
        try:
            if type_of_measurement.lower() in ["uv-pump-mir-probe", "uvmir", "uv/mir", "uv-mir"]:
                self.type_of_measurement = "UV-pump mIR-probe"
                self.xlabel = "wavenumber / $\mathregular{cm^{-1}}$"
                self.ylabel = "t / ps"
                self.zlabel = "$\Delta$mOD"
                self.timescale = "ps"
                self.energyunit = "$\mathregular{cm^{-1}}$"
            elif type_of_measurement.lower() in ["dual solstice", "uv-mir_ds", "uv/mir-ds", "ds"]:
                self.type_of_measurement = "UV-pump mIR-probe (electronically delayed)"
                self.xlabel = "wavenumber / $\mathregular{cm^{-1}}$"
                self.ylabel = "t / ns"
                self.zlabel = "$\Delta$mOD"
                self.timescale = "ns"
                self.energyunit = "$\mathregular{cm^{-1}}$"
            elif type_of_measurement.lower() in ["step-scan", "step scan"]:
                self.type_of_measurement = "step scan"
                self.xlabel = "wavenumber / $\mathregular{cm^{-1}}$"
                self.ylabel = "t / $\mu$s"
                self.zlabel = "$\Delta$ mOD"
                self.timescale = "$\mu$s"
                self.energyunit = "$\mathregular{cm^{-1}}$"
            elif type_of_measurement.lower() in ["transient uvvis", "tas", "uv-pump-vis-probe"]:
                self.type_of_measurement = "UV-pump vis-probe"
                self.xlabel = "$\lambda$ / nm"
                self.ylabel = "t / ps"
                self.zlabel = "$\Delta$mOD"
                self.timescale = "ps"
                self.energyunit = "nm"
            elif type_of_measurement.lower() in ["rapid-scan", "rapid scan"]:
                self.type_of_measurement = "rapid scan"
                self.xlabel = "wavenumber / $\mathregular{cm^{-1}}$"
                self.ylabel = "t / s"
                self.zlabel = "$\Delta$OD"
                self.timescale = "s"
                self.energyunit = "$\mathregular{cm^{-1}}$"
            elif type_of_measurement.lower() in ["spectral dynamics ir", "spec dyn ir", "ir series"]:
                self.type_of_measurement = "IR series"
                self.xlabel = "wavenumber / $\mathregular{cm^{-1}}$"
                self.ylabel = "t / min"
                self.zlabel = "$\Delta$OD"
                self.timescale = "min"
                self.energyunit = "$\mathregular{cm^{-1}}$"
            elif type_of_measurement.lower() in ["product spectra", "paps", "purely absorptive product spectra"]:
                self.type_of_measurement = "product spectra"
                self.xlabel = "wavenumber / $\mathregular{cm^{-1}}$"
                self.ylabel = "t / ps"
                self.zlabel = "$\Delta\Delta$mOD"
                self.timescale = "ps"
                self.energyunit = "$\mathregular{cm^{-1}}$"
            else:
                warnings.warn("Invalid type of measurement. Please check input. For now leaving axes empty...")
                self.xlabel = ""
                self.ylabel = ""
                self.zlabel = ""
                self.timescale = ""
                self.energyunit = ""
        except AttributeError:
            self.xlabel = ""
            self.ylabel = ""
            self.zlabel = ""
            self.timescale = ""
            self.energyunit = ""

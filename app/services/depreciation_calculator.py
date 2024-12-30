class PenyusutanCalculatorServices:
    def __init__(self):
        pass

    def validate_inputs(self, harga_perolehan, estimasi_umur, estimasi_nilai_sisa):
        if not isinstance(harga_perolehan, (int, float)) or harga_perolehan <= 0:
            raise ValueError("Harga Perolehan must be a positive number.")
        if not isinstance(estimasi_umur, (int, float)) or estimasi_umur <= 0:
            raise ValueError("Estimasi Umur Manfaat must be a positive number.")
        if not isinstance(estimasi_nilai_sisa, (int, float)) or estimasi_nilai_sisa < 0:
            raise ValueError("Estimasi Nilai Sisa must be a non-negative number.")

    def straight_line(self, harga_perolehan, estimasi_umur, estimasi_nilai_sisa):
        self.validate_inputs(harga_perolehan, estimasi_umur, estimasi_nilai_sisa)
        biaya_per_tahun = (harga_perolehan - estimasi_nilai_sisa) / estimasi_umur
        biaya_per_bulan = biaya_per_tahun / 12
        return biaya_per_bulan, biaya_per_tahun

    def double_declining(self, harga_perolehan, estimasi_umur, estimasi_nilai_sisa):
        self.validate_inputs(harga_perolehan, estimasi_umur, estimasi_nilai_sisa)
        biaya_per_tahun_list = []
        biaya_per_bulan_list = []

        book_value = harga_perolehan
        for year in range(1, int(estimasi_umur) + 1):
            depreciation = (book_value - estimasi_nilai_sisa) * (2 / estimasi_umur)
            biaya_per_tahun_list.append(depreciation)
            biaya_per_bulan_list.append(depreciation / 12)
            book_value -= depreciation

        return biaya_per_bulan_list, biaya_per_tahun_list

    def calculate(self, harga_perolehan, estimasi_umur, estimasi_nilai_sisa, metode):
        if metode == "straight_line":
            return self.straight_line(harga_perolehan, estimasi_umur, estimasi_nilai_sisa)
        elif metode == "double_declining":
            return self.double_declining(harga_perolehan, estimasi_umur, estimasi_nilai_sisa)
        else:
            raise ValueError("Invalid depreciation method. Choose 'straight_line' or 'double_declining'.")
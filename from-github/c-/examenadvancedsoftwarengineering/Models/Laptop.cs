namespace Laptopreservation.Models
{
    // Definieert de Laptop-entiteit die één laptop uit de webservice/database voorstelt
    public class Laptop
    {
        // Unieke identifier voor elke laptop (Primary Key in de database)
        public int ID { get; set; }

        // Merk van de laptop (bv. Dell, HP, Lenovo)
        public string Brand { get; set; }

        // Modelnaam van de laptop (bv. XPS 13, ThinkPad T14)
        public string Model { get; set; }

        // Prijs van de laptop in euro's (zoals aangeleverd door de webservice)
        public int Price { get; set; }

        // Rating of score van de laptop (kan gebruikt worden voor kwaliteit)
        public int Rating { get; set; }

        // Merk van de processor (bv. Intel, AMD, Apple)
        public string ProcessorBrand { get; set; }

        // Tier/klasse van de processor (bv. i5, i7, Ryzen 7)
        public string ProcessorTier { get; set; }

        // Aantal fysieke processorkernen
        public int NumCores { get; set; }

        // Aantal threads (virtuele cores met hyperthreading)
        public int NumThreads { get; set; }

        // Grootte van het RAM-geheugen (in GB)
        public int RamMemory { get; set; }

        // Type van primaire opslag (bv. SSD, HDD)
        public string PrimaryStorageType { get; set; }

        // Capaciteit van de primaire opslag (in GB)
        public int PrimaryStorageCapacity { get; set; }

        // Type van secundaire opslag (optioneel: bv. SSD, HDD, kan leeg zijn)
        public string SecondaryStorageType { get; set; }

        // Capaciteit van de secundaire opslag (in GB, kan 0 zijn als er geen is)
        public int SecondaryStorageCapacity { get; set; }

        // Merk van de grafische kaart (bv. NVIDIA, AMD, Intel)
        public string GpuBrand { get; set; }

        // Type/model van de GPU (bv. RTX 3060, Radeon RX 6600)
        public string GpuType { get; set; }

        // True als het een touchscreen laptop is, anders false
        public bool IsTouchScreen { get; set; }

        // Grootte van het scherm in inch (bv. 15.6)
        public decimal DisplaySize { get; set; }

        // Resolutie breedte (bv. 1920 pixels)
        public int ResolutionWidth { get; set; }

        // Resolutie hoogte (bv. 1080 pixels)
        public int ResolutionHeight { get; set; }

        // Besturingssysteem van de laptop (bv. Windows 11, Linux, macOS)
        public string OS { get; set; }

        // Aantal jaren garantie op de laptop
        public int YearOfWarranty { get; set; }
    }
}

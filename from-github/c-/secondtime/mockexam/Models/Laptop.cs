namespace mockexam.Models
{

    public class Laptop
    {

        public int Id { get; set; }
        public string Brand { get; set; } 
        public string Model { get; set; } 
        public int Price { get; set; }
        public int Rating { get; set; }
        public string ProcessorBrand { get; set; }
        public string ProcessorTier { get; set; }
        public int NumCores { get; set; }
        public int NumThreads { get; set; }
        public int RamMemory { get; set; }

        public string PrimaryStorageType { get; set; }
        public int PrimaryStorageCapacity { get; set; }
        public string SecondaryStorageType { get; set; }
        public int SecondaryStorageCapacity { get; set; }
        public string GPUBrand { get; set; }
        public string GPUType { get; set; }
        public bool IsTouchScreen { get; set; }
        public decimal DisplaySize { get; set; }
        public int ResolutionWidth { get; set; }
        public int ResolutionHeight { get; set; }
        public string OS { get; set; }
        public int YearOfWarranty { get; set; }

        public override string ToString()
        {
            return $"Laptop ID {Id}: {Brand} {Model}, Price: {Price:EUR}, Rating: {Rating}, Processor: {ProcessorBrand} {ProcessorTier}, RAM: {RamMemory}GB, Storage: {PrimaryStorageType} {PrimaryStorageCapacity}GB, GPU: {GPUBrand} {GPUType}, Touchscreen: {IsTouchScreen}, Display: {DisplaySize} inches, Resolution: {ResolutionWidth}x{ResolutionHeight}, OS: {OS}, Warranty: {YearOfWarranty} years";
        }
    


   }  
}

using mockexam.Models;
using mockexam.Repositories;

namespace mockexam.Service
{
    public class LaptopService : ILaptopService
    {   
        // Field to store the repository, set only in the constructor
        private readonly ILaptopRepository _laptopRepository;

        // Constructor to inject the repository dependency

        // Constructor - receives a repository instance from outside (dependency injection)
        public LaptopService(ILaptopRepository laptopRepository)
        {   // // Store the injected repository so we can use it in other methods
            _laptopRepository = laptopRepository;
        }


        // Method to retrieve all laptops

        public List<Laptop> GetAllLaptops()

        {  //    // Delegate the call to the repository, which retrieves laptops from the data source
            return _laptopRepository.GetAllLaptops();
        }

        
    }
}

   
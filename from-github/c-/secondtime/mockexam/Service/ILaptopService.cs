using mockexam.Models;
using mockexam.Repositories;
using System.Collections.Generic;
namespace mockexam.Service

{
    public interface ILaptopService
    {
        List<Laptop> GetAllLaptops();

        
    }
}
declare module "cachios" {
  import { AxiosInstance } from "axios";

  namespace Cachios {
    function create(
      axiosInstance: AxiosInstance,
      cacheConfig?: any
    ): AxiosInstance;
  }
  export default Cachios;
}

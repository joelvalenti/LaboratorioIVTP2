package labivtp2valenti;

import entities.Pais;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;
import java.util.List;
import javax.persistence.EntityManager;
import javax.persistence.EntityManagerFactory;
import javax.persistence.Persistence;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

public class LabIVtp2Valenti {

    public static void main(String[] args) {

        EntityManagerFactory emf = Persistence.createEntityManagerFactory("LabIVtp2ValentiPU");
        EntityManager em = emf.createEntityManager();
        
        JSONParser parser = new JSONParser();
        String datosJson = "https://restcountries.eu/rest/v2/callingcode/";
        Pais pais = new Pais();
        
        for (int i = 1; i <= 300; i++) {
            
            try {
                
                URL link = new URL(datosJson + i);
                URLConnection yc = link.openConnection();
                BufferedReader in = new BufferedReader(new InputStreamReader(yc.getInputStream()));
                JSONArray arrjson = (JSONArray) parser.parse(in.readLine());
                
                if (arrjson != null) {
                    for (Object object : arrjson) {
                        em.getTransaction().begin();
                        JSONObject paisJson = (JSONObject) object;
                        if (paisJson.get("name").toString().length() <= 50) {
                            pais.setNombrePais((String) paisJson.get("name"));
                        } else {
                            pais.setNombrePais((String) paisJson.get("name").toString().substring(50));
                        }
                        pais.setCodigoPais((long) i);
                        pais.setCapitalPais((String) paisJson.get("capital"));
                        pais.setPoblacion((Long) paisJson.get("population"));
                        pais.setRegion((String) paisJson.get("region"));
                        List coorGeo = (List) paisJson.get("latlng");
                        pais.setLatitud((double) coorGeo.get(0));
                        pais.setLongitud((double) coorGeo.get(1));
                        em.merge(pais);
                        em.flush();
                        em.getTransaction().commit();
                    }
                    System.out.println("Pais encontrado, código: " + i);
                } else {
                    continue;
                }
                in.close();
            } catch (Exception e) {
                System.out.println("No existe un pais con el código: " + i);
            }
        }
        em.close();
        emf.close();
        System.gc();
    }
}

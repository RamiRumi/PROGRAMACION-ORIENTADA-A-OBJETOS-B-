// Ejemplo 1: Sistema básico de automóvil
class Coche {
    private String marca;
    private String modelo;
    private int año;
    private boolean encendido;
    
    public Coche(String marca, String modelo, int año) {
        this.marca = marca;
        this.modelo = modelo;
        this.año = año;
        this.encendido = false;
    }
    
    public void encender() {
        if (!encendido) {
            encendido = true;
            System.out.println("El coche ha sido encendido");
        } else {
            System.out.println("El coche ya está encendido");
        }
    }
    
    public void apagar() {
        if (encendido) {
            encendido = false;
            System.out.println("El coche ha sido apagado");
        } else {
            System.out.println("El coche ya está apagado");
        }
    }
    
    public String getMarca() { return marca; }
    public String getModelo() { return modelo; }
    public int getAño() { return año; }
    public boolean isEncendido() { return encendido; }
}

// Clase principal que ejecuta todo
public class Main {
    public static void main(String[] args) {
        Coche miCoche = new Coche("Toyota", "Corolla", 2022);
        
        System.out.println("Marca: " + miCoche.getMarca());
        System.out.println("Modelo: " + miCoche.getModelo());
        System.out.println("Año: " + miCoche.getAño());
        
        miCoche.encender();
        miCoche.encender();
        miCoche.apagar();
    }
}
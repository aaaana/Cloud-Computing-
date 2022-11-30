import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Scanner;

public class GenerateRandomNumbers {
    public static void main(String[] args) {
        System.out.println("How many random numbers to generate:");   // we use 1000000 to test
        Scanner input = new Scanner(System.in);
        int RandomNumCount = input.nextInt();

        System.out.println("What's the radius?");   //we use 200 to test
        int radius = input.nextInt();
        int diameter = radius * 2;
        input.close();

        try {

            // it creates file input4
            File file = new File("./PiCalculationInput");
            file.createNewFile();

            // Prepare input data 
            FileWriter writer = new FileWriter(file);
            //writer.write(radius + "\r\n");
            //writer.write(System.getProperty("line.separator"));

            for (int i = 0; i < RandomNumCount; i++) {
                int xvalue = (int) (Math.random() * diameter);
                int yvalue = (int) (Math.random() * diameter);
                writer.write("(" + xvalue + "," + yvalue + ") ");
            }

            // send the data into the file
            writer.flush();

            // closing the write after pushing the data inside the .txt file
            writer.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}

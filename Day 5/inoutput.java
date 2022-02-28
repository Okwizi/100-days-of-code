import java.util.Scanner;
public class input {
	public static void main(String[] args){
	String name;
	Scanner scan = new Scanner(System.in);
	name = scan.nextLine();
	System.out.print("Enter your name: ");

	System.out.println("Welcome "+ name);
	}
}
// The same intent, in Java.
import java.util.*;

public class Concentration {
  record Holding(String symbol, double weight) {}

  public static void main(String[] args) {
    List<Holding> holdings = List.of(
      new Holding("AAPL", 0.52),
      new Holding("MSFT", 0.31),
      new Holding("GLD", 0.17)
    );

    for (Holding holding : holdings) {
      if (holding.weight() > 0.35) {
        System.out.println(
          "Concentrated: " + holding.symbol()
        );
      }
    }
  }
}

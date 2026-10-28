package example;

/* metamodel_version: 1.12.0 */
/* version: 2026-10-28 */
import java.net.URI;
import java.time.LocalDate;
import java.time.LocalTime;
import java.time.ZonedDateTime;
import java.util.List;
import lombok.*;

/**
  An output that a reusable workflow or an action declares for the job or step that calls it to read.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public abstract class GhaOutput  {

  private String description;
  private String outputExpression;
  private String outputId;


}
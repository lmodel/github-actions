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
  An input that a reusable workflow or an action declares, under the key a caller writes in its `with` map.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public abstract class GhaInput  {

  private String description;
  private String inputId;
  private String default_;
  private Boolean required;


}
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
  The field that says whether a caller must supply a value.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class GhaRequiredMixin  {

  private Boolean required;


}
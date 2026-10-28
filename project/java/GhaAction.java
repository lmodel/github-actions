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
  An action: a directory whose `action.yml` or `action.yaml` file names its inputs, its outputs and the runtime that executes it. A workflow step runs it with `uses`.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class GhaAction  {

  private List<GhaActionInput> inputs;
  private List<GhaActionOutput> outputs;
  private URI actionUri;
  private String actionPath;
  private String using;


}
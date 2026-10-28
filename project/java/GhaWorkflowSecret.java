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
  A secret under a reusable workflow's `on.workflow_call.secrets` key, by name; its value is never recorded.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class GhaWorkflowSecret  {

  private String description;
  private String secretId;
  private Boolean required;


}
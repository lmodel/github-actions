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
  An input under a reusable workflow's `on.workflow_call.inputs` key.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class GhaWorkflowInput extends GhaInput {

  private String inputType;


}
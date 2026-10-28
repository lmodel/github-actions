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
  An output under a reusable workflow's `on.workflow_call.outputs` key, set from an output of one of its jobs.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class GhaWorkflowOutput extends GhaOutput {



}
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
  A workflow that other workflows call as a job, because its `on` key names `workflow_call`; it declares the inputs, outputs and secrets its callers pass and read.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class GhaReusableWorkflow extends GhaWorkflow {

  private List<GhaWorkflowInput> inputs;
  private List<GhaWorkflowOutput> outputs;
  private List<GhaWorkflowSecret> secrets;


}